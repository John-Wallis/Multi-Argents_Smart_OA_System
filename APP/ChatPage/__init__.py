"""Chat page package consolidating chat-related blueprints."""
from __future__ import annotations

from flask import Flask

from .ChatPage import chat_page_bp
from .ConversationController import conversation_controller_bp
from .UserController import user_controller_bp

__all__ = [
    "register_chatpage_blueprints",
    "chat_page_bp",
    "conversation_controller_bp",
    "user_controller_bp",
]


def register_chatpage_blueprints(app: Flask) -> None:
    """Register all chat-related blueprints with the provided app."""
    app.register_blueprint(chat_page_bp, url_prefix="/chat")
    app.register_blueprint(user_controller_bp, url_prefix="/chat/users")
    app.register_blueprint(
        conversation_controller_bp, url_prefix="/chat/conversations"
    )
