"""Security-focused tests: headers, host enforcement, input hardening, escaping."""

import importlib

import pytest

import app as app_module


@pytest.fixture()
def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


def test_security_headers_present(client):
    r = client.get("/")
    h = r.headers
    assert "Content-Security-Policy" in h
    assert "script-src 'self'" in h["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in h["Content-Security-Policy"]
    assert h["X-Content-Type-Options"] == "nosniff"
    assert h["X-Frame-Options"] == "DENY"
    assert h["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Strict-Transport-Security" in h


def test_reflected_url_is_escaped_not_executed(client):
    token = app_module._encode_ranked(["Kindness"])
    r = client.get(f'/result?ranked={token}&x="><script>alert(1)</script>')
    body = r.get_data(as_text=True)
    assert "<script>alert(1)" not in body
    assert "&lt;script&gt;" in body or "%3Cscript%3E" in body


def test_oversized_ranked_input_is_bounded(client):
    # A pathologically long token must not error or hang; it's rejected by the
    # length cap and treated as no selection.
    r = client.get("/result?ranked=" + "A" * 100000)
    assert r.status_code == 400


def test_malformed_token_rejected(client):
    # injection-y junk isn't valid base64url -> decodes to nothing -> 400
    r = client.get("/result?ranked=__import__;DROP TABLE;<b>")
    assert r.status_code == 400
    assert b"DROP TABLE" not in r.data


def test_host_allowlist_blocks_spoofed_host(monkeypatch):
    monkeypatch.setenv("ALLOWED_HOSTS", "good.example.com")
    importlib.reload(app_module)
    client = app_module.app.test_client()
    assert client.get("/", headers={"Host": "evil.example.com"}).status_code == 400
    assert client.get("/", headers={"Host": "good.example.com"}).status_code == 200
    # restore default app for other test modules
    monkeypatch.delenv("ALLOWED_HOSTS", raising=False)
    importlib.reload(app_module)


def test_host_open_when_allowlist_unset(client):
    # Dev default: no allow-list configured -> any host accepted.
    assert client.get("/", headers={"Host": "anything.test"}).status_code == 200
