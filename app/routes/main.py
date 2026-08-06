"""
General application routes.

Provides basic endpoints used to verify that the
application is running correctly.
"""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    """
    Return a "welcome" message

    Returns:
        str: A message indicating that the API is running.
    """
    return "Customer Support API is running"

@main_bp.get("/health")
def health():
    """
    Check the application health status.

    Returns:
        tuple: A JSON response with the application status
        and the corresponding HTTP status code.
    """
    return {"status": "Ok"}, 200

