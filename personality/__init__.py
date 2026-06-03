"""Personality engine: map a ranked values list onto a personality profile.

Public API:
    build_personality(ranked)  -> full profile dict
    value_names()              -> list of all value names
    classify(emphasis)         -> archetype ranking for a Schwartz emphasis vector
    archetype_geometry(arch)   -> compass/radar geometry for one archetype
    resonant_values(arch, n)   -> values most aligned with an archetype
    ARCHETYPES / archetype_by_key -> the archetype catalogue
"""

from .archetypes import ARCHETYPES, archetype_by_key
from .profile import (
    archetype_geometry,
    build_personality,
    classify,
    rank_weights,
    resonant_values,
    value_names,
)

__all__ = [
    "ARCHETYPES",
    "archetype_by_key",
    "archetype_geometry",
    "build_personality",
    "classify",
    "rank_weights",
    "resonant_values",
    "value_names",
]
