"""Route registration for user controller."""
from __future__ import annotations

from flask import Blueprint


def register_routes(blueprint: Blueprint) -> None:
    """Attach user controller routes."""
    from .profile import register as register_profile

    register_profile(blueprint)
