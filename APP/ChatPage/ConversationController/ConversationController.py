"""Blueprint for managing chat conversations."""
from __future__ import annotations

from flask import Blueprint, render_template

from .routes import register_routes


conversation_controller_bp = Blueprint(
    "conversation_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
)

register_routes(conversation_controller_bp)

__all__ = ["conversation_controller_bp"]
