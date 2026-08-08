from flask import Blueprint

from app.schemas.document_schema import document_types_schema
from app.services.document_services import DocumentTypeService


document_type_bp = Blueprint("document_types", __name__, url_prefix="/document-types")


@document_type_bp.get("/")
def get_document_types():
    """
    Retrieve all available document types.
    """
    document_types = DocumentTypeService.get_all()

    return document_types_schema.dump(document_types), 200