# Production image for the Values-Based Personality Test.
# Python pinned to 3.12 to match the nix-shell dev environment (Python 3.12.8).
# Hardening: for full supply-chain integrity, pin the base image by digest, e.g.
#   FROM python:3.12-slim@sha256:<digest>
# (resolve with `docker buildx imagetools inspect python:3.12-slim`).
FROM python:3.12-slim

# Don't write .pyc files; flush stdout/stderr immediately for clean logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code.
COPY values.py wsgi.py app.py ./
COPY personality/ ./personality/
COPY templates/ ./templates/
COPY static/ ./static/

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 9000 

# 3 workers is a reasonable default; tune via $WEB_CONCURRENCY if desired.
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "3", "wsgi:app"]
