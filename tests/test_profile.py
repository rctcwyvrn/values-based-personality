"""Tests for the personality scoring/classification pipeline."""

import math

import pytest

from personality import (
    ARCHETYPES,
    archetype_geometry,
    build_personality,
    rank_weights,
    resonant_values,
    value_names,
)
from personality.archetypes import archetype_by_key
from personality.dimensions import BIG_FIVE, SCHWARTZ, compute_baseline
from personality.profile import _aggregate, _emphasis, classify
from values import VALUES


# --- data integrity --------------------------------------------------------

def test_value_count_and_uniqueness():
    names = value_names()
    assert len(names) == 100
    assert len(set(names)) == 100


def test_value_ids_unique_and_byte_sized():
    ids = [v["id"] for v in VALUES]
    assert len(ids) == len(set(ids)), "ids must be unique"
    # one byte each, so they fit the base64 token encoding
    assert all(isinstance(i, int) and 0 <= i <= 255 for i in ids)


@pytest.mark.parametrize("value", VALUES, ids=[v["name"] for v in VALUES])
def test_loadings_sum_to_one(value):
    for framework, keys in (("schwartz", SCHWARTZ), ("big_five", BIG_FIVE)):
        d = value[framework]
        assert abs(sum(d.values()) - 1.0) < 1e-9
        assert set(d).issubset(set(keys))
        assert all(w >= 0 for w in d.values())


def test_baseline_sums_to_one():
    base = compute_baseline(VALUES)
    assert abs(sum(base["schwartz"].values()) - 1.0) < 1e-9
    assert abs(sum(base["big_five"].values()) - 1.0) < 1e-9


# --- rank weighting --------------------------------------------------------

def test_rank_weights_normalised_and_decreasing():
    w = rank_weights(10)
    assert abs(sum(w) - 1.0) < 1e-9
    assert all(w[i] > w[i + 1] for i in range(len(w) - 1))
    assert w[0] > w[-1]


def test_rank_weights_edge_cases():
    assert rank_weights(0) == []
    assert rank_weights(1) == [1.0]


def test_rank_weights_are_top_heavy():
    # power weighting makes the #1 pick carry more than the linear 1/(n) ramp
    w = rank_weights(10)
    assert w[0] > 0.25  # linear would give 10/55 ~= 0.18


def test_sharpen_pivots_at_baseline():
    from personality.profile import _sharpen, EMPHASIS_GAMMA
    out = _sharpen({"a": 1.0, "b": 2.0, "c": 0.5})
    assert EMPHASIS_GAMMA > 1.0
    assert out["a"] == 1.0          # baseline is a fixed point
    assert out["b"] > 2.0           # above average amplified
    assert out["c"] < 0.5           # below average suppressed


def test_rank_order_matters():
    """Putting an achievement value first vs last shifts the raw vector."""
    first = _aggregate(["Ambition", "Kindness"], "schwartz", SCHWARTZ)
    last = _aggregate(["Kindness", "Ambition"], "schwartz", SCHWARTZ)
    assert first["achievement"] > last["achievement"]
    assert last["benevolence"] > first["benevolence"]


def test_aggregate_sums_to_one():
    vec = _aggregate(["Adventure", "Creativity", "Curiosity"], "schwartz", SCHWARTZ)
    assert abs(sum(vec.values()) - 1.0) < 1e-9


def test_unknown_value_raises():
    with pytest.raises(KeyError):
        _aggregate(["Not A Value"], "schwartz", SCHWARTZ)


# --- classification face validity -----------------------------------------

def _primary_key(ranked):
    return build_personality(ranked)["classification"]["primary"]["key"]


def test_caregiving_values_classify_as_caregiver():
    ranked = ["Kindness", "Compassion", "Generosity", "Service", "Warmth"]
    assert _primary_key(ranked) == "caregiver"


def test_achievement_values_classify_as_achiever():
    ranked = ["Ambition", "Mastery", "Power", "Status", "Influence"]
    assert _primary_key(ranked) == "achiever"


def test_exploration_values_classify_as_explorer_or_freespirit():
    ranked = ["Adventure", "Excitement", "Daring", "Spontaneity", "Freedom"]
    assert _primary_key(ranked) in {"explorer", "free_spirit"}


def test_justice_values_classify_as_idealist():
    ranked = ["Justice", "Equality", "Fairness", "Diversity"]
    assert _primary_key(ranked) == "idealist"


def test_security_values_classify_as_guardian():
    ranked = ["Stability", "Safety", "Order", "Duty", "Reliability"]
    assert _primary_key(ranked) == "guardian"


# --- structural guarantees of the full profile ----------------------------

def test_build_personality_shape():
    profile = build_personality(["Kindness", "Creativity", "Adventure"])
    assert set(profile) == {
        "ranked",
        "classification",
        "big_five",
        "schwartz",
        "higher_order",
        "compass",
        "conflict_note",
    }
    assert len(profile["big_five"]) == 5
    assert len(profile["schwartz"]) == 10
    assert len(profile["higher_order"]) == 4
    # classification ranks every archetype
    assert len(profile["classification"]["ranked"]) == 10


def test_compass_angle_in_range():
    profile = build_personality(["Adventure", "Curiosity"])
    assert 0.0 <= profile["compass"]["angle"] < 360.0
    assert profile["compass"]["magnitude"] >= 0.0


def test_big_five_sorted_descending():
    profile = build_personality(["Leadership", "Ambition", "Power"])
    emph = [t["emphasis"] for t in profile["big_five"]]
    assert emph == sorted(emph, reverse=True)


def test_confidence_band_values():
    profile = build_personality(["Kindness", "Compassion", "Generosity"])
    assert profile["classification"]["confidence"] in {"clear", "leaning", "blended"}


def test_empty_ranked_raises():
    with pytest.raises(ValueError):
        build_personality([])


# --- archetype catalogue + geometry ---------------------------------------

def test_every_archetype_has_required_fields():
    keys = {a["key"] for a in ARCHETYPES}
    assert len(ARCHETYPES) == 10
    assert len(keys) == 10
    for a in ARCHETYPES:
        for field in (
            "name", "emoji", "tagline", "portrait", "recognize", "two_truths",
            "thriving", "empty", "kryptonite", "green_flags", "red_flags",
            "quick_stats", "schwartz", "axis_change", "axis_focus",
            "big_five_profile", "detail", "strengths", "tensions",
            "opposite", "neighbors",
        ):
            assert field in a, f"{a['key']} missing {field}"
        assert a["emoji"], "emoji present"
        assert a["portrait"] and a["recognize"], "casual content present"
        assert a["green_flags"] and a["red_flags"], "flags present"


def test_quick_stats_well_formed():
    for a in ARCHETYPES:
        assert a["quick_stats"], f"{a['key']} has no quick stats"
        for s in a["quick_stats"]:
            assert set(s) == {"label", "level"}
            assert isinstance(s["level"], int) and 1 <= s["level"] <= 5


def test_casual_copy_is_jargon_free():
    jargon = [
        "schwartz", "circumplex", "self-transcendence", "self-enhancement",
        "openness to change", "conservation", "emphasis", "ocean", "cosine",
    ]
    for a in ARCHETYPES:
        casual = (
            a["portrait"] + a["recognize"] + a["green_flags"] + a["red_flags"]
            + [a["two_truths"], a["thriving"], a["empty"], a["kryptonite"]]
        )
        text = " ".join(casual).lower()
        hits = [j for j in jargon if j in text]
        assert not hits, f"{a['key']} casual copy leaks jargon: {hits}"
        assert a["detail"], "detail paragraphs present"
        assert a["strengths"] and a["tensions"]


def test_archetype_relationships_are_valid_keys():
    keys = {a["key"] for a in ARCHETYPES}
    for a in ARCHETYPES:
        assert a["opposite"] in keys
        assert a["opposite"] != a["key"]
        for n in a["neighbors"]:
            assert n in keys and n != a["key"]


def test_archetype_geometry_shape():
    arch = archetype_by_key("caregiver")
    geo = archetype_geometry(arch)
    assert len(geo["schwartz"]) == 10
    assert len(geo["higher_order"]) == 4
    assert 0.0 <= geo["compass"]["angle"] < 360.0


def test_resonant_values_face_validity():
    caregiver = resonant_values(archetype_by_key("caregiver"))
    assert "Kindness" in caregiver or "Compassion" in caregiver
    achiever = resonant_values(archetype_by_key("achiever"))
    assert any(v in achiever for v in ("Ambition", "Mastery", "Status", "Power"))


def test_conflict_note_for_opposing_values():
    """Mixing strong self-enhancement and self-transcendence flags a conflict."""
    ranked = ["Power", "Ambition", "Status", "Justice", "Equality", "Compassion"]
    profile = build_personality(ranked)
    # Not asserting it always triggers, but if both poles are high it must fire.
    ho = {h["key"]: h["emphasis"] for h in profile["higher_order"]}
    if ho["self_enhancement"] >= 1.15 and ho["self_transcendence"] >= 1.15:
        assert profile["conflict_note"] is not None
