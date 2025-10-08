"""Application configuration module."""
from __future__ import annotations

import os
from pathlib import Path


class Config:
    """Base configuration shared by the entire project."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    INSTANCE_PATH = Path(__file__).resolve().parent / "instance"
