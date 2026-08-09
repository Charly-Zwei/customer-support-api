"""
Purchase Service
"""
from decimal import Decimal
from sqlalchemy import select
from app.extensions import db
from app.models import Purchase
from app.services.customer_services import CustomerService


class PurchaseService:
    @staticmethod
    def create_purchase(
        customer_id: int,
        amount: Decimal,
        description: str
    ) -> Purchase:
        """
         Creates a new purchase.

        Args:
            customer_id: Customer identifier.
            amount: Purchase amount.
            description: Purchase description.

        Returns:
            Purchase: The created purchase.

        Raises:
            ValueError: If the customer does not exist,
                the amount is invalid.
        """
        customer = CustomerService.get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        purchase = Purchase(
            customer_id=customer_id,
            amount=amount,
            description=description
        )
        try:
            db.session.add(purchase)
            db.session.commit()
            return purchase
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_purchase_by_id(
        purchase_id: int
    ) -> Purchase | None:
        """
        Retrieves a purchase by its ID.

        Args:
            purchase_id: Purchase identifier.

        Returns:
            Purchase | None: The purchase if found, otherwise None.
        """
        return db.session.get(
            Purchase,
            purchase_id
        )

    @staticmethod
    def get_customer_purchases(
        customer_id: int
    ) -> list[Purchase]:
        """
        Retrieves all purchases for a customer.

        Args:
            customer_id: Customer identifier.

        Returns:
            list[Purchase]: Customer purchases ordered by purchase date
        """
        customer = CustomerService.get_customer_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found")

        statement = (
            select(Purchase)
            .where(Purchase.customer_id == customer_id)
            .order_by(Purchase.purchase_date.desc())
        )
        return db.session.scalars(statement).all()

    @staticmethod
    def get_all_purchases() -> list[Purchase]:
        """
        Retrieves all purchases.

        Returns:
            list[Purchase]: All purchases ordered by purchase date.
        """
        statement = (
            select(Purchase)
            .order_by(Purchase.purchase_date.desc())
        )
        return db.session.scalars(statement).all()