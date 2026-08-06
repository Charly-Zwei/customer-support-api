"""
Application extensions.

Creates shared Flask extensions that are initialized inside 
the application factory.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()