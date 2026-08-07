from app.extensions import db

class DocumentType (db.Model):
    """
    Represents the availables documents types
    """

    __tablename__ = "document_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    customers = db.relationship(
        "Customer",
        back_populates="document_types",
        lazy=True
    )

    def __repr__(self) -> str:
        return f"DocumentType {self.name}"