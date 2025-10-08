"""DataPanel module containing routes and related assets."""
from __future__ import annotations

from flask import Blueprint

from .DataPanel import data_panel_bp

__all__ = ["data_panel_bp"]
