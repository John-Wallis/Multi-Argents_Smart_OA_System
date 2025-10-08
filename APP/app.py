"""Flask application entry-point."""
from __future__ import annotations

from flask import Flask

from .config import Config
from .ChatPage import register_chatpage_blueprints
from .DataPanel import data_panel_bp


def create_app() -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Register blueprints for the different application modules.
    app.register_blueprint(data_panel_bp, url_prefix="/data")
    register_chatpage_blueprints(app)

    return app


def main() -> None:
    """Run the application in development mode."""
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
