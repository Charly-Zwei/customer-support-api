"""
Application Factory

This module builds and configures the Flask Application.
Responsabilities:
- Create the Flask Application
- load configuration
- Initialize extensions
- Register Blueprints
"""


from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes.main import main_bp
from .routes.customer_routes import customer_bp
from .routes.purchase_routes import purchase_bp
from .routes.report_routes import report_bp

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

    from app import models

    #Blueprint Initializer
    app.register_blueprint(main_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(report_bp)
    return app