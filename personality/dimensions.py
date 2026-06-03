"""Dimension definitions for the two personality frameworks, plus the geometry
that turns a Schwartz value-vector into a position on the circumplex compass.

The Schwartz values are laid out on a circle in their canonical order so that
opposing motivations sit roughly opposite one another:

    self_direction (0deg) -> stimulation -> hedonism -> achievement -> power
    -> security -> conformity -> tradition -> benevolence -> universalism (324deg)

The two bipolar axes fall out of that layout:
    * Openness-to-Change (self_direction/stimulation) vs Conservation
      (security/conformity/tradition)
    * Self-Enhancement (achievement/power) vs Self-Transcendence
      (benevolence/universalism)
"""

from __future__ import annotations

import math

# Canonical circular order of the 10 Schwartz basic values.
SCHWARTZ = [
    "self_direction",
    "stimulation",
    "hedonism",
    "achievement",
    "power",
    "security",
    "conformity",
    "tradition",
    "benevolence",
    "universalism",
]

BIG_FIVE = [
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "emotional_stability",
]

# Human-readable labels for display.
SCHWARTZ_LABELS = {
    "self_direction": "Self-Direction",
    "stimulation": "Stimulation",
    "hedonism": "Hedonism",
    "achievement": "Achievement",
    "power": "Power",
    "security": "Security",
    "conformity": "Conformity",
    "tradition": "Tradition",
    "benevolence": "Benevolence",
    "universalism": "Universalism",
}

BIG_FIVE_LABELS = {
    "openness": "Openness",
    "conscientiousness": "Conscientiousness",
    "extraversion": "Extraversion",
    "agreeableness": "Agreeableness",
    "emotional_stability": "Emotional Stability",
}

# The four higher-order Schwartz quadrants and the basic values they contain.
# Hedonism straddles Openness-to-Change and Self-Enhancement, so it is shared.
HIGHER_ORDER = {
    "openness_to_change": ["self_direction", "stimulation", "hedonism"],
    "self_enhancement": ["achievement", "power", "hedonism"],
    "conservation": ["security", "conformity", "tradition"],
    "self_transcendence": ["benevolence", "universalism"],
}

HIGHER_ORDER_LABELS = {
    "openness_to_change": "Openness to Change",
    "self_enhancement": "Self-Enhancement",
    "conservation": "Conservation",
    "self_transcendence": "Self-Transcendence",
}

# Angle (radians) of each Schwartz value around the circumplex, evenly spaced
# in canonical order starting from 0 (pointing right / East).
SCHWARTZ_ANGLES = {
    key: math.radians(i * 360.0 / len(SCHWARTZ)) for i, key in enumerate(SCHWARTZ)
}


def empty_schwartz() -> dict[str, float]:
    return {k: 0.0 for k in SCHWARTZ}


def empty_big_five() -> dict[str, float]:
    return {k: 0.0 for k in BIG_FIVE}


def compute_baseline(values: list[dict]) -> dict[str, dict[str, float]]:
    """Mean loading vector across all values, per framework.

    This is the profile a perfectly average / random selection would produce.
    Because the value set is skewed (prosocial values are common), comparing a
    user's profile against this baseline is what reveals what is *distinctive*
    about their choices rather than what is merely common in the value set.

    Each returned vector sums to 1.0 (since every value's loadings sum to 1.0).
    """
    n = len(values)
    sz = empty_schwartz()
    b5 = empty_big_five()
    for v in values:
        for k, w in v["schwartz"].items():
            sz[k] += w
        for k, w in v["big_five"].items():
            b5[k] += w
    return {
        "schwartz": {k: sz[k] / n for k in SCHWARTZ},
        "big_five": {k: b5[k] / n for k in BIG_FIVE},
    }


def compass_coords(schwartz_emphasis: dict[str, float]) -> dict[str, float]:
    """Project an emphasis vector onto the 2D circumplex.

    Returns x/y (cartesian), angle (degrees, 0 = East, counter-clockwise) and
    magnitude (how far from the centre — i.e. how pronounced the lean is).
    """
    x = sum(schwartz_emphasis[k] * math.cos(SCHWARTZ_ANGLES[k]) for k in SCHWARTZ)
    y = sum(schwartz_emphasis[k] * math.sin(SCHWARTZ_ANGLES[k]) for k in SCHWARTZ)
    angle = math.degrees(math.atan2(y, x)) % 360.0
    magnitude = math.hypot(x, y)
    return {"x": x, "y": y, "angle": angle, "magnitude": magnitude}
