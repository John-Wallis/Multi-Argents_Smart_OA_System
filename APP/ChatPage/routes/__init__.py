"""Route registration for the chat page blueprint."""
from __future__ import annotations

from flask import Blueprint


def register_routes(blueprint: Blueprint) -> None:
    """Attach all chat page routes to the blueprint."""
    from .home import register as register_home

    register_home(blueprint)
