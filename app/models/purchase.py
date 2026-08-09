from datetime import datetime, UTC
from app.extensions import db

class Purchase(db.Model):
    """
    Represents a customer purchase
    """

    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key = True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    purchase_date = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        index=True
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    #Amount Constraint
    __table_args__ = (
        db.CheckConstraint(
            "amount > 0",
            name="check_amount_positive"
        ),
    )

    description = db.Column(
        db.String(255),
        nullable=True
    )

    customer = db.relationship(
        "Customer",
        back_populates="purchases"
    )

    def __repr__(self) -> str:
        return f"Purchase {self.id}"