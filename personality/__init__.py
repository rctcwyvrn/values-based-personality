"""Personality engine: map a ranked values list onto a personality profile.

Public API:
    build_personality(ranked)  -> full profile dict
    value_names()              -> list of all value names
    classify(emphasis)         -> archetype ranking for a Schwartz emphasis vector
    archetype_geometry(arch)   -> compass/radar geometry for one archetype
    resonant_values(arch, n)   -> values most aligned with an archetype
    ARCHETYPES / archetype_by_key -> the archetype catalogue

Science-page helpers:
    signature, axis_positions, archetype_big_five, anti_resonant_values,
    most_confusable, rarity, circle_positions
"""

from .archetypes import ARCHETYPES, archetype_by_key
from .profile import (
    anti_resonant_values,
    archetype_big_five,
    archetype_geometry,
    axis_positions,
    build_personality,
    circle_positions,
    classify,
    most_confusable,
    rank_weights,
    rarity,
    resonant_values,
    signature,
    value_names,
)

__all__ = [
    "ARCHETYPES",
    "anti_resonant_values",
    "archetype_big_five",
    "archetype_by_key",
    "archetype_geometry",
    "axis_positions",
    "build_personality",
    "circle_positions",
    "classify",
    "most_confusable",
    "rank_weights",
    "rarity",
    "resonant_values",
    "signature",
    "value_names",
]
