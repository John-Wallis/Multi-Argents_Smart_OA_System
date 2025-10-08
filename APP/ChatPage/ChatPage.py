"""Blueprint for general chat page views."""
from __future__ import annotations

from flask import Blueprint, render_template

from .routes import register_routes


chat_page_bp = Blueprint(
    "chat_page",
    __name__,
    template_folder="templates",
    static_folder="static",
)

register_routes(chat_page_bp)

__all__ = ["chat_page_bp"]
