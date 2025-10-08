"""Blueprint definition for the data panel section."""
from __future__ import annotations

from flask import Blueprint, render_template

from .routes import register_routes


data_panel_bp = Blueprint(
    "data_panel",
    __name__,
    template_folder="templates",
    static_folder="static",
)

register_routes(data_panel_bp)


__all__ = ["data_panel_bp"]
