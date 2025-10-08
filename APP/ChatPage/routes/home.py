"""Home route for the chat page."""
from __future__ import annotations

from flask import render_template


def register(blueprint):
    """Register the chat home page route."""

    @blueprint.route("/")
    def chat_home():
        return render_template("chat_page/index.html")
