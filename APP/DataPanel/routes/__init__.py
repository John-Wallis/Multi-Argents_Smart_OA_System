"""Route registration helpers for the data panel."""
from __future__ import annotations

from flask import Blueprint


def register_routes(blueprint: Blueprint) -> None:
    """Register all routes for the data panel blueprint."""
    from .dashboard import register as register_dashboard

    register_dashboard(blueprint)
