"""Route-level tests for the Flask app."""

import pytest

from app import app as flask_app
from personality import ARCHETYPES


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


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
    r = client.get("/result?ranked=Kindness,Compassion,Generosity")
    assert r.status_code == 200
    assert b"/types/caregiver" in r.data
    assert b"The Caregiver" in r.data


def test_result_has_copy_share_section(client):
    r = client.get("/result?ranked=Kindness,Compassion,Generosity")
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


def test_result_ignores_invalid_names(client):
    r = client.get("/result?ranked=Bogus,Kindness,Compassion")
    assert r.status_code == 200
    assert b"The Caregiver" in r.data


def test_result_offers_edit_link_with_ranking(client):
    r = client.get("/result?ranked=Adventure,Curiosity,Freedom")
    assert r.status_code == 200
    # the edit link carries the ranking back to the picker
    assert b"ranked=Adventure" in r.data


def test_picker_restores_ranking_from_url(client):
    r = client.get("/?ranked=Adventure,Curiosity,Bogus,Freedom")
    assert r.status_code == 200
    # invalid names dropped, valid order preserved in the data-initial seed
    assert b'data-initial="Adventure,Curiosity,Freedom"' in r.data


def test_picker_caps_ranking_at_max(client):
    many = ",".join(v["name"] for v in __import__("values").VALUES[:20])
    r = client.get("/?ranked=" + many)
    assert r.status_code == 200
