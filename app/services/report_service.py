from datetime import datetime, timedelta, UTC
from sqlalchemy import select, func
from sqlalchemy.engine import Row
from app.extensions import db
from app.models import Customer, Purchase, DocumentType

LOYAL_CUSTOMER_THRESHOLD = 5_000_000
LOYALTY_PERIOD_DAYS = 30

class ReportService:
    """
    Business logic for report generation
    """

    @staticmethod
    def get_loyal_customers_report() -> list[Row]:
        """
        Retrieves customers whose purchases in the last
        30 days exceed the loyalty threshold.

        Returns:
            list: Report rows containing customer data and
                total purchase amount.
        """

        thirty_days_ago = datetime.now(UTC) - timedelta(days=LOYALTY_PERIOD_DAYS)

        statement = (
            select(
                DocumentType.name.label("document_type"),
                Customer.document_number,
                Customer.first_name,
                Customer.last_name,
                Customer.email,
                Customer.phone,
                func.sum(Purchase.amount).label("total_amount")
            )
            .join(Customer.purchases)
            .join(Customer.document_type)
            .where(
                Purchase.purchase_date >= thirty_days_ago
            )
            .group_by(
                Customer.id,
                DocumentType.name,
                Customer.document_number,
                Customer.first_name,
                Customer.last_name,
                Customer.email,
                Customer.phone
            )
            .having(
                func.sum(Purchase.amount) > LOYAL_CUSTOMER_THRESHOLD
            )
            .order_by(
                func.sum(Purchase.amount).desc()
            )
        )

        return db.session.execute(statement).all()