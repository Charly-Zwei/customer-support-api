"""
Application Factory

This module builds and cofigures the Flask Application.
Responsabilities:
- Create Flask
- load configuration
- Initialize extensions
- Register Blueprints
"""


from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes.main import main_bp

def create_app():
    """
    Create and configure the flask application.

    Returns:
        Flask: A fully configured flask application
    """
    app = Flask(__name__)

    #Configuration
    app.config.from_object(Config)
    db.init_app(app)

    #Flask-Migrate
    migrate.init_app(app, db)

    #Blueprint Initializer
    app.register_blueprint(main_bp)

    return app