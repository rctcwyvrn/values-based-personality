"""Route-level tests for the Flask app."""

import html

import pytest

from app import _encode_ranked
from app import app as flask_app
from personality import ARCHETYPES


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def tok(*names):
    return _encode_ranked(list(names))


def test_index_lists_values(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Values-Based Personality Test" in r.data


def test_index_has_about_section(client):
    body = client.get("/").get_data(as_text=True)
    assert 'id="about"' in body
    # the three frameworks are explained
    assert "Acceptance and Commitment Therapy" in body
    assert "Schwartz" in body and "circumplex" in body
    assert "Big Five" in body
    assert "Why combine all three?" in body


def test_types_index(client):
    r = client.get("/types")
    assert r.status_code == 200
    # every archetype is linked from the index
    for a in ARCHETYPES:
        assert f'/types/{a["key"]}'.encode() in r.data
        assert a["name"].encode() in r.data


@pytest.mark.parametrize("arch", ARCHETYPES, ids=[a["key"] for a in ARCHETYPES])
def test_each_casual_type_page_renders(client, arch):
    r = client.get(f'/types/{arch["key"]}')
    assert r.status_code == 200
    body = html.unescape(r.get_data(as_text=True))
    assert arch["name"] in body
    # casual page shows the portrait + recognize, links to related + the science
    assert arch["portrait"][0][:30] in body
    assert arch["recognize"][0] in body
    # the new casual blocks all render
    assert arch["two_truths"] in body
    assert arch["thriving"] in body
    assert arch["empty"] in body
    assert arch["kryptonite"] in body
    assert arch["green_flags"][0] in body
    assert arch["red_flags"][0] in body
    assert arch["quick_stats"][0]["label"] in body
    assert "qs-pip on" in body  # at least one filled meter pip
    assert f'/types/{arch["opposite"]}' in body
    assert f'/types/{arch["key"]}/science' in body


@pytest.mark.parametrize("arch", ARCHETYPES, ids=[a["key"] for a in ARCHETYPES])
def test_each_science_page_renders(client, arch):
    r = client.get(f'/types/{arch["key"]}/science')
    assert r.status_code == 200
    body = html.unescape(r.get_data(as_text=True))
    assert arch["name"] in body
    # the technical content lives here now
    assert "circumplex" in body
    assert arch["detail"][0][:30] in body
    assert arch["axis_change"]["note"][:30] in body
    # the new A/B/C sections all render
    assert "Motivational signature" in body
    assert "Big Five signature" in body
    assert "Where it sits on the two axes" in body
    assert "Values that pull away" in body
    assert "Where it sits among all twelve" in body  # all-types compass
    assert "of random value-rankings land here" in body  # rarity stat
    assert "most blended with" in body  # confusable stat
    assert "vs" in body  # faceoff heading
    assert "/methods" in body  # link to methodology
    # links back to the casual page
    assert f'/types/{arch["key"]}"' in body


def test_methods_page_renders(client):
    body = html.unescape(client.get("/methods").get_data(as_text=True))
    assert "How this test works" in body
    assert "Acceptance and Commitment Therapy" in body  # pipeline step 1
    assert "Glossary" in body
    assert "The research behind it" in body  # citations
    assert "Schwartz, S. H. (1992)" in body
    assert "A worked example" in body
    # nav link present site-wide
    assert "/methods" in body


def test_nav_has_methods_link(client):
    assert "/methods" in client.get("/").get_data(as_text=True)


def test_unknown_type_404(client):
    assert client.get("/types/not-a-type").status_code == 404


def test_unknown_science_page_404(client):
    assert client.get("/types/not-a-type/science").status_code == 404


def test_compass_map_dots_do_not_overlap():
    import math

    from app import _circle_map
    dots = _circle_map("explorer")["dots"]
    assert len(dots) == 12
    # every glyph is < 24px wide; min-gap spreading must keep centres clear
    nearest = min(
        math.hypot(a["x"] - b["x"], a["y"] - b["y"])
        for i, a in enumerate(dots)
        for b in dots[i + 1:]
    )
    assert nearest > 24, f"compass dots too close: {nearest:.1f}px"


def test_spread_angles_enforces_min_gap():
    from app import _spread_angles
    spread = sorted(_spread_angles([3.2, 5.8, 32.4, 53.0, 125.4]))
    gaps = [(spread[i + 1] - spread[i]) for i in range(len(spread) - 1)]
    assert all(g >= 16 - 1e-6 for g in gaps), gaps


def test_result_from_url_links_to_type_page(client):
    r = client.get("/result?ranked=" + tok("Kindness", "Compassion", "Generosity"))
    assert r.status_code == 200
    assert b"/types/caregiver" in r.data
    assert b"The Caregiver" in r.data


def test_roundtrip_encode_decode():
    names = ["Adventure", "Curiosity", "Freedom", "Creativity"]
    token = _encode_ranked(names)
    # token is a compact base64url string (no commas, no padding)
    assert "," not in token and "=" not in token
    from app import _decode_ranked
    assert _decode_ranked(token) == names


def test_token_encodes_stable_ids_not_positions():
    import base64

    from values import VALUES
    id_by_name = {v["name"]: v["id"] for v in VALUES}
    names = ["Ambition", "Kindness"]
    token = _encode_ranked(names)
    pad = "=" * (-len(token) % 4)
    raw = list(base64.urlsafe_b64decode(token + pad))
    # token bytes are the values' explicit ids, in ranking order — so a future
    # reordering of values.py would not change this token.
    assert raw == [id_by_name["Ambition"], id_by_name["Kindness"]]


def test_result_has_copy_share_section(client):
    r = client.get("/result?ranked=" + tok("Kindness", "Compassion", "Generosity"))
    body = r.get_data(as_text=True)
    assert 'id="share"' in body
    assert 'data-share="copy"' in body  # clipboard copy button
    # snappy message names the type with its emoji
    assert "The Caregiver" in body
    assert "🤲" in body
    # no direct-to-social-media intent links anymore
    assert "twitter.com/intent" not in body
    assert "facebook.com/sharer" not in body
    assert "linkedin.com/sharing" not in body


def test_result_requires_values(client):
    assert client.get("/result").status_code == 400
    assert client.get("/result?ranked=").status_code == 400


def test_result_rejects_malformed_token(client):
    # non-base64 junk decodes to nothing -> treated as no selection
    assert client.get("/result?ranked=not,a,token!!").status_code == 400


def test_result_offers_edit_link_with_ranking(client):
    token = tok("Adventure", "Curiosity", "Freedom")
    r = client.get("/result?ranked=" + token)
    assert r.status_code == 200
    # the edit link carries the same token back to the picker
    assert ("ranked=" + token).encode() in r.data


def test_picker_restores_ranking_from_url(client):
    token = tok("Adventure", "Curiosity", "Freedom")
    r = client.get("/?ranked=" + token)
    assert r.status_code == 200
    # decoded back to names (in order) for the picker's data-initial seed
    assert b'data-initial="Adventure,Curiosity,Freedom"' in r.data


def test_picker_caps_ranking_at_max(client):
    names = [v["name"] for v in __import__("values").VALUES[:20]]
    r = client.get("/?ranked=" + _encode_ranked(names))
    assert r.status_code == 200
    # only the first MAX_PICKS survive decoding
    import re
    seed = re.search(r'data-initial="([^"]*)"', r.get_data(as_text=True)).group(1)
    assert len(seed.split(",")) == 10
