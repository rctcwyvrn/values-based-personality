"""Route-level tests for the Flask app."""

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


def test_types_index(client):
    r = client.get("/types")
    assert r.status_code == 200
    # every archetype is linked from the index
    for a in ARCHETYPES:
        assert f'/types/{a["key"]}'.encode() in r.data
        assert a["name"].encode() in r.data


@pytest.mark.parametrize("arch", ARCHETYPES, ids=[a["key"] for a in ARCHETYPES])
def test_each_type_page_renders(client, arch):
    r = client.get(f'/types/{arch["key"]}')
    assert r.status_code == 200
    assert arch["name"].encode() in r.data
    # axis framing and related-type links are present
    assert arch["axis_change"]["pole"].encode() in r.data
    assert f'/types/{arch["opposite"]}'.encode() in r.data


def test_unknown_type_404(client):
    assert client.get("/types/not-a-type").status_code == 404


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
