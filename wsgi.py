"""Gunicorn entry point: ``gunicorn -b 0.0.0.0:8000 wsgi:app``."""

from app import app

__all__ = ["app"]
