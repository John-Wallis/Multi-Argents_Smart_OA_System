"""Blueprint for user related chat operations."""
from __future__ import annotations

from flask import Blueprint, render_template

from .routes import register_routes


user_controller_bp = Blueprint(
    "user_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
)

register_routes(user_controller_bp)

__all__ = ["user_controller_bp"]
