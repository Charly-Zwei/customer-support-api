"""
Application Configuration.

Loads environmental variables and defines the applications's 
configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print("DATABASE_URL:", os.getenv("DATABASE_URL"))