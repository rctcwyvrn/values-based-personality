"""Flask app: rank your top values, get a personality reading.

    flask --app app run --debug      # development
    gunicorn -b 0.0.0.0:8000 wsgi:app  # production (see wsgi.py)
"""

from __future__ import annotations

import math
import os

from flask import Flask, abort, render_template, request

# Content-Security-Policy. Scripts are locked to same-origin files (no inline
# scripts anywhere), which is the meaningful XSS mitigation. Inline *style*
# attributes (bar widths) require 'unsafe-inline' for style-src only. The form
# only ever GETs to ourselves; the page is never framed.
_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'"
)

from personality import (
    ARCHETYPES,
    archetype_by_key,
    archetype_geometry,
    build_personality,
    resonant_values,
)
from personality.dimensions import SCHWARTZ, SCHWARTZ_ANGLES, SCHWARTZ_LABELS
from values import VALUES

MAX_PICKS = 10

# Emphasis ratio mapped to the outer edge of the radar (values above this clamp).
RADAR_FULL_SCALE = 2.5


def _radar_geometry(schwartz: list[dict], size: int = 320, margin: int = 70) -> dict:
    """Build SVG point/axis geometry for the Schwartz emphasis radar.

    ``schwartz`` is profile["schwartz"] (one dict per dimension with an
    'emphasis' ratio). Returns the polygon points and per-axis label anchors,
    in a coordinate system where y grows downward (SVG convention).
    """
    center = size / 2
    max_r = center - margin
    by_key = {d["key"]: d for d in schwartz}

    points = []
    axes = []
    for key in SCHWARTZ:
        angle = SCHWARTZ_ANGLES[key]
        emphasis = by_key[key]["emphasis"]
        r = max_r * min(emphasis / RADAR_FULL_SCALE, 1.0)
        # Invert y so larger angles go counter-clockwise visually.
        px = center + r * math.cos(angle)
        py = center - r * math.sin(angle)
        points.append((round(px, 1), round(py, 1)))

        # Axis spoke endpoints and a label anchor just beyond the rim.
        ex = center + max_r * math.cos(angle)
        ey = center - max_r * math.sin(angle)
        lx = center + (max_r + 24) * math.cos(angle)
        ly = center - (max_r + 24) * math.sin(angle)
        anchor = "middle"
        if lx < center - 5:
            anchor = "end"
        elif lx > center + 5:
            anchor = "start"
        axes.append(
            {
                "label": SCHWARTZ_LABELS[key],
                "ex": round(ex, 1),
                "ey": round(ey, 1),
                "lx": round(lx, 1),
                "ly": round(ly, 1),
                "anchor": anchor,
            }
        )

    polygon = " ".join(f"{x},{y}" for x, y in points)
    return {
        "size": size,
        "center": center,
        "max_r": max_r,
        "polygon": polygon,
        "axes": axes,
        # Reference ring at emphasis == 1.0 (the "average" baseline).
        "baseline_r": round(max_r * (1.0 / RADAR_FULL_SCALE), 1),
    }


def _parse_ranked(raw: str) -> list[str]:
    """Parse a comma-separated ranking, keeping only valid, unique names.

    Order is preserved (it *is* the ranking) and capped at MAX_PICKS. Used for
    both the ?ranked= query param on the result/picker pages and any form post.
    """
    valid = {v["name"] for v in VALUES}
    seen: set[str] = set()
    out: list[str] = []
    # Bound the input before splitting: 10 names is < 200 chars, so anything
    # beyond this is malformed/abusive and we refuse to do work proportional
    # to a giant query string (defence-in-depth against DoS).
    for name in raw[:1000].split(","):
        name = name.strip()
        if name and name in valid and name not in seen:
            seen.add(name)
            out.append(name)
            if len(out) >= MAX_PICKS:
                break
    return out


def _share_message(primary: dict, page_url: str) -> dict:
    """Build a short, snappy share message for the clipboard.

    The page URL already encodes the ranking, so pasting the message anywhere
    shares the result. ``text`` is the snappy headline (shown on the page);
    ``message`` is what gets copied (headline + link). share.js rebuilds the
    message from the live browser URL.
    """
    emoji = primary.get("emoji", "")
    text = f"{emoji} I'm {primary['name']} on the Values-Based Personality Test. What's your type?"
    return {
        "emoji": emoji,
        "text": text,
        "url": page_url,
        "message": f"{text}\n{page_url}",
    }


def create_app() -> Flask:
    app = Flask(__name__)

    # Cap request bodies. The app has no large uploads; this is defence in depth.
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024

    # Only honour X-Forwarded-* when explicitly placed behind a trusted proxy,
    # so the proxy headers can't be spoofed by direct clients (set TRUST_PROXY=1).
    if os.environ.get("TRUST_PROXY") == "1":
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Host allow-list neutralises Host-header injection into the absolute share
    # URLs / og:url. Set ALLOWED_HOSTS="example.com,www.example.com" in prod;
    # when unset (dev) any host is accepted.
    allowed_hosts = {
        h.strip().lower()
        for h in os.environ.get("ALLOWED_HOSTS", "").split(",")
        if h.strip()
    }

    @app.before_request
    def _enforce_host():
        if allowed_hosts and request.host.split(":")[0].lower() not in allowed_hosts:
            abort(400)

    @app.after_request
    def _security_headers(resp):
        resp.headers.setdefault("Content-Security-Policy", _CSP)
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        resp.headers.setdefault(
            "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
        )
        # Honoured only over HTTPS; harmless (ignored) over plain HTTP in dev.
        resp.headers.setdefault(
            "Strict-Transport-Security", "max-age=63072000; includeSubDomains"
        )
        return resp

    @app.route("/")
    def index():
        initial = _parse_ranked(request.args.get("ranked", ""))
        return render_template(
            "select.html",
            values=VALUES,
            max_picks=MAX_PICKS,
            initial_ranked=initial,
        )

    @app.route("/result")
    def result():
        ranked = _parse_ranked(request.args.get("ranked", ""))

        if not ranked:
            return render_template(
                "select.html",
                values=VALUES,
                max_picks=MAX_PICKS,
                initial_ranked=[],
                error="Please choose and rank at least one value.",
            ), 400

        profile = build_personality(ranked)
        radar = _radar_geometry(profile["schwartz"])
        return render_template(
            "result.html",
            profile=profile,
            radar=radar,
            ranked_param=",".join(ranked),
            share=_share_message(profile["classification"]["primary"], request.url),
        )

    @app.route("/types")
    def types():
        return render_template("types.html", archetypes=ARCHETYPES)

    @app.route("/types/<key>")
    def archetype(key):
        arch = archetype_by_key(key)
        if arch is None:
            abort(404)
        geometry = archetype_geometry(arch)
        radar = _radar_geometry(geometry["schwartz"])
        related = {
            "opposite": archetype_by_key(arch["opposite"]),
            "neighbors": [archetype_by_key(k) for k in arch["neighbors"]],
        }
        return render_template(
            "type.html",
            arch=arch,
            geometry=geometry,
            radar=radar,
            related=related,
            resonant=resonant_values(arch),
        )

    return app


app = create_app()
