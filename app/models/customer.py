from datetime import datetime, UTC
from app.extensions import db

class Customer(db.Model):
    """
    Represents a customer in the system
    """

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    document_type_id = db.Column(
        db.Integer,
        db.ForeignKey("document_types.id"),
        nullable=False
    )
    document_number = db.Column(
        db.String(30),
        nullable=False
    )
    first_name = db.Column(
        db.String(100),
        nullable=False
    )
    last_name = db.Column(
        db.String(100),
        nullable=False
    )
    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
        index=True
    )
    phone = db.Column(
        db.String(20),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC)
    )
    document_type = db.relationship(
        "DocumentType",
        back_populates="customers"
    )
    purchases = db.relationship(
        "Purchase",
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy=True
    )

    # The combination of document type and document number must be unique.
    # Ex: CC 123456 != TI 123456
    __table_args__ = (
        db.UniqueConstraint(
            "document_type_id",
            "document_number",
            name="uq_customer_document"
        ),
    )

    def __repr__(self) -> str:
        return f"Customer: {self.first_name} {self.last_name}"