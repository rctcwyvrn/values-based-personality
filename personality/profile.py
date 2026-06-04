"""Turn a ranked top-N values list into a personality profile.

Pipeline:
    1. rank-weight the chosen values (earlier picks count for more)
    2. aggregate their loadings into a raw Schwartz and Big Five vector
    3. normalise against the random-selection baseline -> an *emphasis* vector
       that captures what is distinctive about the choices
    4. match the emphasis vector to the nearest archetype(s) by cosine
       similarity, and project it onto the circumplex compass
    5. describe the Big Five emphasis in plain language
"""

from __future__ import annotations

import math
import random

from values import VALUES

from .archetypes import ARCHETYPES
from .dimensions import (
    BIG_FIVE,
    BIG_FIVE_LABELS,
    HIGHER_ORDER,
    HIGHER_ORDER_LABELS,
    SCHWARTZ,
    SCHWARTZ_LABELS,
    compass_coords,
    compute_baseline,
)

# Index values by name for quick lookup.
_BY_NAME = {v["name"]: v for v in VALUES}
_BASELINE = compute_baseline(VALUES)

# --- "spikiness" knobs -----------------------------------------------------
# RANK_WEIGHT_EXPONENT shapes how much top picks dominate: weights are
# (n - rank) ** exponent, so 1.0 is the old linear ramp and >1 makes the first
# choices count for more. EMPHASIS_GAMMA sharpens the final emphasis vector,
# pivoting at the baseline (1.0): values above average inflate, below average
# shrink, so a profile reads with sharper peaks and deeper valleys. Both are
# pure dials — raise them for spikier results, set to 1.0 to restore the flat
# behaviour.
RANK_WEIGHT_EXPONENT = 2.0
EMPHASIS_GAMMA = 1.25


def value_names() -> list[str]:
    return [v["name"] for v in VALUES]


def rank_weights(n: int) -> list[float]:
    """Decay weights for n ranked picks, normalised to sum to 1.

    Weight for rank i is (n - i) ** RANK_WEIGHT_EXPONENT, so the #1 pick gets
    the most and the last the least. The exponent controls how top-heavy the
    curve is (1.0 = linear; higher = first choices dominate more).
    """
    if n <= 0:
        return []
    raw = [(n - i) ** RANK_WEIGHT_EXPONENT for i in range(n)]
    total = float(sum(raw))
    return [r / total for r in raw]


def _sharpen(emphasis: dict[str, float]) -> dict[str, float]:
    """Raise contrast by exponentiating emphasis, pivoting at the baseline.

    emphasis == 1.0 (exactly average) is a fixed point; above-average
    dimensions are amplified and below-average ones suppressed, so the profile
    becomes spikier without changing the ordering of dimensions.
    """
    return {k: v ** EMPHASIS_GAMMA for k, v in emphasis.items()}


def _aggregate(ranked: list[str], framework: str, keys: list[str]) -> dict[str, float]:
    """Rank-weighted sum of the chosen values' loadings for one framework."""
    weights = rank_weights(len(ranked))
    vec = {k: 0.0 for k in keys}
    for name, w in zip(ranked, weights):
        value = _BY_NAME.get(name)
        if value is None:
            raise KeyError(f"Unknown value: {name!r}")
        for k, load in value[framework].items():
            vec[k] += w * load
    return vec


def _emphasis(raw: dict[str, float], baseline: dict[str, float]) -> dict[str, float]:
    """Ratio of observed mass to baseline mass, per dimension.

    1.0 means exactly as emphasised as a random selection; >1 over-expressed,
    <1 under-expressed. This removes the value set's built-in skew.
    """
    return {k: (raw[k] / baseline[k] if baseline[k] > 0 else 0.0) for k in raw}


def _cosine(a: dict[str, float], b: dict[str, float], keys: list[str]) -> float:
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(a[k] ** 2 for k in keys))
    nb = math.sqrt(sum(b[k] ** 2 for k in keys))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _archetype_emphasis(proto: dict[str, float]) -> dict[str, float]:
    """Express an archetype prototype in the same baseline-relative space."""
    full = {k: proto.get(k, 0.0) for k in SCHWARTZ}
    return _emphasis(full, _BASELINE["schwartz"])


def _schwartz_emphasis_of(loadings: dict[str, float]) -> dict[str, float]:
    """Baseline-relative emphasis vector for any raw Schwartz loading dict."""
    full = {k: loadings.get(k, 0.0) for k in SCHWARTZ}
    return _emphasis(full, _BASELINE["schwartz"])


def _schwartz_sorted(emphasis: dict[str, float], raw: dict[str, float]) -> list[dict]:
    return sorted(
        (
            {
                "key": k,
                "label": SCHWARTZ_LABELS[k],
                "raw": raw.get(k, 0.0),
                "emphasis": emphasis[k],
            }
            for k in SCHWARTZ
        ),
        key=lambda d: d["emphasis"],
        reverse=True,
    )


def archetype_geometry(arch: dict) -> dict:
    """Compass/radar geometry for an archetype's own prototype vector.

    Lets each type page render the same circumplex radar the result page uses,
    driven by the archetype's defining values rather than a user's picks.
    """
    emphasis = _sharpen(_schwartz_emphasis_of(arch["schwartz"]))
    return {
        "schwartz": _schwartz_sorted(emphasis, arch["schwartz"]),
        "higher_order": higher_order_scores(emphasis),
        "compass": compass_coords(emphasis),
    }


def _value_resonance(arch: dict) -> list[tuple[str, float]]:
    """All values scored by cosine alignment to an archetype, best first."""
    target = _schwartz_emphasis_of(arch["schwartz"])
    scored = [
        (v["name"], _cosine(_schwartz_emphasis_of(v["schwartz"]), target, SCHWARTZ))
        for v in VALUES
    ]
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored


def resonant_values(arch: dict, n: int = 8) -> list[str]:
    """The values most aligned with an archetype ("values that lead here")."""
    return [name for name, _ in _value_resonance(arch)[:n]]


def anti_resonant_values(arch: dict, n: int = 6) -> list[str]:
    """The values *least* aligned with an archetype ("values that pull away")."""
    return [name for name, _ in reversed(_value_resonance(arch)[-n:])]


def signature(arch: dict) -> list[dict]:
    """The archetype's raw prototype weights as labelled percentages."""
    items = sorted(arch["schwartz"].items(), key=lambda kv: kv[1], reverse=True)
    return [
        {"key": k, "label": SCHWARTZ_LABELS[k], "pct": round(w * 100)}
        for k, w in items
    ]


def axis_positions(schwartz: dict[str, float]) -> dict[str, float]:
    """Position on each bipolar axis as a fraction in [0, 1].

    change: 0 = pure Conservation, 1 = pure Openness to Change.
    focus:  0 = pure Self-Transcendence, 1 = pure Self-Enhancement.
    """
    g = lambda k: schwartz.get(k, 0.0)  # noqa: E731
    # Hedonism sits on the Openness side of the circle, so it counts toward the
    # change axis but is left out of the focus axis (where it would wrongly read
    # as self-enhancement).
    openness = g("self_direction") + g("stimulation") + g("hedonism")
    conservation = g("security") + g("conformity") + g("tradition")
    enhancement = g("achievement") + g("power")
    transcendence = g("benevolence") + g("universalism")

    def frac(a: float, b: float) -> float:
        total = a + b
        return 0.5 if total == 0 else a / total

    return {
        "change": frac(openness, conservation),
        "focus": frac(enhancement, transcendence),
    }


def archetype_big_five(arch: dict, n: int = 12) -> list[dict]:
    """A full five-trait Big Five profile for an archetype.

    Derived the same way a user's is: average the Big Five loadings of the
    values that most resonate with this type, normalise against the baseline,
    and sharpen. Returns all five traits, sorted, with band labels.
    """
    raw = {k: 0.0 for k in BIG_FIVE}
    for name in resonant_values(arch, n):
        for k, load in _BY_NAME[name]["big_five"].items():
            raw[k] += load
    total = sum(raw.values()) or 1.0
    raw = {k: v / total for k, v in raw.items()}
    return describe_big_five(_sharpen(_emphasis(raw, _BASELINE["big_five"])))


def most_confusable(arch: dict) -> dict:
    """The other archetype this one is most easily blended with."""
    target = _sharpen(_archetype_emphasis(arch["schwartz"]))
    best = None
    for other in ARCHETYPES:
        if other["key"] == arch["key"]:
            continue
        sim = _cosine(target, _sharpen(_archetype_emphasis(other["schwartz"])), SCHWARTZ)
        if best is None or sim > best[1]:
            best = (other, sim)
    return {"archetype": best[0], "similarity": round(best[1] * 100)}


def circle_positions() -> list[dict]:
    """Compass angle of every archetype, for the all-types mini-map."""
    out = []
    for a in ARCHETYPES:
        emph = _sharpen(_schwartz_emphasis_of(a["schwartz"]))
        out.append(
            {
                "key": a["key"],
                "name": a["name"],
                "emoji": a["emoji"],
                "angle": compass_coords(emph)["angle"],
            }
        )
    return out


_RARITY_CACHE: dict[str, float] = {}


def _rarity_table(trials: int = 4000, seed: int = 20240601) -> dict[str, float]:
    """Fraction of random value-rankings that land on each archetype.

    A seeded Monte-Carlo estimate, computed once and cached. Lazy so it costs
    nothing until a science page is first viewed.
    """
    if not _RARITY_CACHE:
        rng = random.Random(seed)
        names = [v["name"] for v in VALUES]
        counts = {a["key"]: 0 for a in ARCHETYPES}
        for _ in range(trials):
            k = rng.randint(5, 10)
            pick = rng.sample(names, k)
            counts[build_personality(pick)["classification"]["primary"]["key"]] += 1
        _RARITY_CACHE.update({k: v / trials for k, v in counts.items()})
    return _RARITY_CACHE


def rarity(arch: dict) -> dict:
    """How common this archetype is among random rankings, with a tier label."""
    pct = _rarity_table()[arch["key"]] * 100
    if pct >= 15:
        tier = "common"
    elif pct >= 8:
        tier = "fairly common"
    elif pct >= 4:
        tier = "uncommon"
    else:
        tier = "rare"
    return {"pct": round(pct, 1), "tier": tier}


def classify(schwartz_emphasis: dict[str, float]) -> dict:
    """Rank archetypes by similarity to the emphasis vector.

    Returns the primary and secondary archetype, a confidence band, and the
    full ranked list of (archetype, similarity) for transparency.
    """
    scored = []
    for arch in ARCHETYPES:
        # Sharpen the archetype side too, so the cosine compares like with like
        # when the caller passes a sharpened user emphasis.
        proto = _sharpen(_archetype_emphasis(arch["schwartz"]))
        sim = _cosine(schwartz_emphasis, proto, SCHWARTZ)
        scored.append((arch, sim))
    scored.sort(key=lambda t: t[1], reverse=True)

    primary, s1 = scored[0]
    secondary, s2 = scored[1]
    gap = s1 - s2
    if gap >= 0.15:
        confidence = "clear"
    elif gap >= 0.05:
        confidence = "leaning"
    else:
        confidence = "blended"

    return {
        "primary": primary,
        "secondary": secondary,
        "confidence": confidence,
        "gap": gap,
        "ranked": [
            {"archetype": a, "similarity": s} for a, s in scored
        ],
    }


# Band cutoffs, expressed in raw-emphasis terms but raised to the sharpening
# exponent so the *labels* trigger at the same underlying emphasis as before
# (a raw 1.5 still reads "high"), even though the displayed number is sharpened.
_BAND_HIGH = 1.5 ** EMPHASIS_GAMMA
_BAND_ELEVATED = 1.15 ** EMPHASIS_GAMMA
_BAND_MUTED = 0.85 ** EMPHASIS_GAMMA
_BAND_LOW = 0.6 ** EMPHASIS_GAMMA


def _band(emphasis: float) -> str:
    """Label a (sharpened) emphasis ratio as high / elevated / low / typical."""
    if emphasis >= _BAND_HIGH:
        return "high"
    if emphasis >= _BAND_ELEVATED:
        return "elevated"
    if emphasis <= _BAND_LOW:
        return "low"
    if emphasis <= _BAND_MUTED:
        return "muted"
    return "typical"


def describe_big_five(big_five_emphasis: dict[str, float]) -> list[dict]:
    """Per-trait readout, sorted from most to least emphasised."""
    out = []
    for k in BIG_FIVE:
        e = big_five_emphasis[k]
        out.append(
            {
                "key": k,
                "label": BIG_FIVE_LABELS[k],
                "emphasis": e,
                "band": _band(e),
            }
        )
    out.sort(key=lambda d: d["emphasis"], reverse=True)
    return out


def higher_order_scores(schwartz_emphasis: dict[str, float]) -> list[dict]:
    """Aggregate emphasis into the four higher-order quadrants for display."""
    out = []
    for key, members in HIGHER_ORDER.items():
        score = sum(schwartz_emphasis[m] for m in members) / len(members)
        out.append(
            {
                "key": key,
                "label": HIGHER_ORDER_LABELS[key],
                "emphasis": score,
            }
        )
    out.sort(key=lambda d: d["emphasis"], reverse=True)
    return out


def conflict_note(higher_order: list[dict]) -> str | None:
    """Flag a profile that emphasises opposing quadrants at once.

    Opposite pairs on the circumplex: openness_to_change vs conservation, and
    self_enhancement vs self_transcendence. Strongly favouring both ends of an
    axis signals a complex / internally-tensioned value set.
    """
    by_key = {h["key"]: h["emphasis"] for h in higher_order}
    pairs = [
        ("openness_to_change", "conservation"),
        ("self_enhancement", "self_transcendence"),
    ]
    for a, b in pairs:
        if by_key[a] >= 1.15 and by_key[b] >= 1.15:
            la = HIGHER_ORDER_LABELS[a]
            lb = HIGHER_ORDER_LABELS[b]
            return (
                f"Your values pull strongly toward both {la} and {lb}, "
                "which are normally opposing motivations. That points to a complex, "
                "multi-sided personality that holds tension rather than "
                "resolving it."
            )
    return None


def build_personality(ranked: list[str]) -> dict:
    """Full pipeline: ranked value names -> complete personality profile."""
    if not ranked:
        raise ValueError("Need at least one ranked value.")

    schwartz_raw = _aggregate(ranked, "schwartz", SCHWARTZ)
    big_five_raw = _aggregate(ranked, "big_five", BIG_FIVE)

    # Raw emphasis (ratio to baseline), then a sharpened copy for display and
    # classification. Conflict detection runs on the *raw* higher-order scores
    # so its calibrated 1.15 threshold keeps the same meaning.
    schwartz_raw_emphasis = _emphasis(schwartz_raw, _BASELINE["schwartz"])
    big_five_raw_emphasis = _emphasis(big_five_raw, _BASELINE["big_five"])
    schwartz_emphasis = _sharpen(schwartz_raw_emphasis)
    big_five_emphasis = _sharpen(big_five_raw_emphasis)

    classification = classify(schwartz_emphasis)
    big_five = describe_big_five(big_five_emphasis)
    higher_order = higher_order_scores(schwartz_emphasis)
    compass = compass_coords(schwartz_emphasis)

    schwartz_sorted = _schwartz_sorted(schwartz_emphasis, schwartz_raw)

    return {
        "ranked": ranked,
        "classification": classification,
        "big_five": big_five,
        "schwartz": schwartz_sorted,
        "higher_order": higher_order,
        "compass": compass,
        "conflict_note": conflict_note(higher_order_scores(schwartz_raw_emphasis)),
    }
