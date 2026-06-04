# Values-Based Personality Test

Rank your top personal values and get a personality reading. A Flask + Jinja
web app that maps a ranked top-10 from a list of 100 ACT-framework values onto
the **Schwartz values circumplex** (the geometric engine) and the **Big Five**
(the descriptive language), then classifies you into one of twelve archetypes.

## How it works

```
ranked values ──▶ rank-weight ──▶ aggregate loadings ──▶ normalise vs. baseline
                                                                │
                          ┌─────────────────────────────────────┤
                          ▼                                     ▼
              nearest archetype (cosine)            Big Five emphasis readout
                  + circumplex compass                  + conflict detection
```

1. Each of the 100 values in [`values.py`](values.py) is tagged with loadings on
   the 10 Schwartz basic values and the 5 Big Five traits (each set sums to 1.0).
2. Your ranked picks are **rank-weighted** (first choice counts most) and summed.
3. The result is **normalised against the average selection**, so the reading
   reflects what is *distinctive* about your choices rather than the value set's
   built-in prosocial skew.
4. The emphasis vector is matched to the nearest archetype(s) by cosine
   similarity and projected onto the circumplex compass; opposing-quadrant
   tension is flagged as a "complex" profile.

The scoring engine lives in [`personality/`](personality/) and is framework
-agnostic (no Flask import), so it is unit-tested on its own.

## Development (Nix)

`shell.nix` pins nixpkgs to an exact commit, so every shell has identical
package versions (Python 3.12, Flask 3.0.3, gunicorn 23.0.0, pytest 8.3.3).

```sh
nix-shell                       # enter the pinned dev environment
flask --app app run --debug     # http://127.0.0.1:5000
pytest                          # run the test suite
```

## Deployment (Docker)

The image installs pinned runtime deps from `requirements.txt` (mirroring the
nix versions) and serves with gunicorn as a non-root user.

```sh
docker build -t values-personality-test .
docker run --rm -p 8000:8000 values-personality-test   # http://localhost:8000
```

Tune worker count with `-e WEB_CONCURRENCY=…` or by editing the `CMD` in the
[`Dockerfile`](Dockerfile).

## Layout

| Path | Purpose |
|------|---------|
| `values.py` | The 100 values with Schwartz + Big Five loadings |
| `personality/dimensions.py` | Framework definitions, baseline, circumplex geometry |
| `personality/archetypes.py` | The twelve archetype prototypes |
| `personality/profile.py` | Scoring, classification, description |
| `app.py` / `wsgi.py` | Flask app factory and gunicorn entrypoint |
| `templates/`, `static/` | Jinja templates, CSS, drag-to-rank JS |
| `tests/` | Pytest suite for the scoring engine |
