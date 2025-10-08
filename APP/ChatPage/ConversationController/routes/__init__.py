"""Route registration for conversation controller."""
from __future__ import annotations

from flask import Blueprint


def register_routes(blueprint: Blueprint) -> None:
    """Attach conversation controller routes."""
    from .history import register as register_history

    register_history(blueprint)
