

from __future__ import annotations

import base64
import binascii
import math
import os
import re

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
# Raised from 2.5 to give sharpened (spikier) profiles headroom before they
# clamp to the rim — see EMPHASIS_GAMMA in personality/profile.py.
RADAR_FULL_SCALE = 3.5


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


# Stable id <-> name maps. Each value carries an explicit, frozen ``id`` (see
# values.py) so the URL token is independent of the list's ordering — reordering
# or extending values.py never changes existing links. The ranking is encoded
# as base64url of the value ids (one byte each, ids being < 256), giving a
# short, opaque token instead of a long comma-separated list of names.
_NAME_BY_ID = {v["id"]: v["name"] for v in VALUES}
_ID_BY_NAME = {v["name"]: v["id"] for v in VALUES}
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]*$")


def _encode_ranked(names: list[str]) -> str:
    """Encode a ranking (ordered value names) as a base64url token of ids."""
    raw = bytes(_ID_BY_NAME[n] for n in names if n in _ID_BY_NAME)
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _decode_ranked(token: str) -> list[str]:
    """Decode a base64url token back to an ordered, validated list of names.

    Tolerant of junk: anything that isn't a clean token, or that decodes to
    unknown / duplicate ids, is dropped. Order is preserved (it *is* the
    ranking) and capped at MAX_PICKS. Returns [] on any problem.
    """
    token = (token or "").strip()
    # A valid top-MAX_PICKS token is ~14 chars; cap well above that and reject
    # non-alphabet input so we never do work proportional to a giant query.
    if not token or len(token) > 256 or not _TOKEN_RE.match(token):
        return []
    pad = "=" * (-len(token) % 4)
    try:
        raw = base64.urlsafe_b64decode(token + pad)
    except (binascii.Error, ValueError):
        return []

    seen: set[int] = set()
    out: list[str] = []
    for value_id in raw:
        if value_id in _NAME_BY_ID and value_id not in seen:
            seen.add(value_id)
            out.append(_NAME_BY_ID[value_id])
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
        initial = _decode_ranked(request.args.get("ranked", ""))
        return render_template(
            "select.html",
            values=VALUES,
            max_picks=MAX_PICKS,
            initial_ranked=initial,
        )

    @app.route("/result")
    def result():
        ranked = _decode_ranked(request.args.get("ranked", ""))

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
            ranked_param=_encode_ranked(ranked),
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
