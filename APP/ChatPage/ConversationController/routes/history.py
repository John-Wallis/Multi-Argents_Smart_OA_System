"""Conversation history routes."""
from __future__ import annotations

from flask import render_template


def register(blueprint):
    """Register conversation history views."""

    @blueprint.route("/")
    def history_list():
        return render_template("conversation_controller/index.html")
