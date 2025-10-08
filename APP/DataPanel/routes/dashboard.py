"""Dashboard routes for the data panel."""
from __future__ import annotations

from flask import render_template


def register(blueprint):
    """Attach dashboard views to the provided blueprint."""

    @blueprint.route("/")
    def dashboard_home():
        return render_template("data_panel/index.html")
