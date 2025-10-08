"""User profile routes."""
from __future__ import annotations

from flask import render_template


def register(blueprint):
    """Register profile related routes."""

    @blueprint.route("/")
    def profile_list():
        return render_template("user_controller/index.html")
