from sqlalchemy import select

from app.extensions import db
from app.models import DocumentType


class DocumentTypeService:
    """
    Service layer for document type operations.
    """

    @staticmethod
    def get_all() -> list[DocumentType]:
        """
        Retrieve all available document types.

        Returns:
            List of document types.
        """
        statement = select(DocumentType).order_by(DocumentType.name)

        return db.session.scalars(statement).all()