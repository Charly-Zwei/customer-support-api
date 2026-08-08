"""
Customer service.

Contains the business logic related to customer management.
"""

from sqlalchemy import select
from app.extensions import db
from app.models import Customer
from app.models import DocumentType


class CustomerService:
    """
    Handles customer business logic
    """

    @staticmethod
    def get_customer_by_id(customer_id: int) -> Customer | None:
        """
        Retrieve a customer by its ID.

        Args:
            customer_id: Customer identifier.

        Returns:
            Customer if found, otherwise None.
        """
        return db.session.get(Customer, customer_id)

    @staticmethod
    def get_customer_by_document(document_type, document_number: str) -> Customer | None:
        """
        Retrieve a customer by its document number.

        Args:
            document_type: Customer document type.
            document_number: Customer document number.

        Returns:
            Customer if found, otherwise None.
        """
        statement = (
            select(Customer)
            .join(DocumentType)
            .where(
                DocumentType.name == document_type,
                Customer.document_number == document_number
            )
        )

        return db.session.scalar(statement)

    @staticmethod
    def get_customer_by_email(email: str) -> Customer | None:
        """
        Retrieve a customer by email.

        Args:
            email: Customer email address.

        Returns:
            Customer if found, otherwise None.
        """
        statement = select(Customer).where(Customer.email == email)

        return db.session.scalar(statement)

    @staticmethod
    def create_customer(
        document_type_id: int,
        document_number: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
    ) -> Customer:
        """
        Creates a Customer.
        Args:
            document_type_id: Document type identifier.
            document_number: Customer document number.
            first_name: Customer first name.
            last_name: Customer last name.
            email: Customer email address.
            phone: Customer phone number.

        Returns:
            Customer: The newly created customer.

        Raises:
            ValueError: If the document type does not exist, or the
                document number/email is already in use.
        """
        document_type = db.session.get(DocumentType, document_type_id)
        if document_type is None:
            raise ValueError("Document type does not exist.")

        customer = CustomerService.get_customer_by_document(document_number)
        if customer is not None:
            raise ValueError("Document already exists.")

        customer = CustomerService.get_customer_by_email(email=email)
        if customer is not None:
            raise ValueError("Email already exists")

        customer = Customer(
            document_type_id=document_type_id,
            document_number=document_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        try:
            db.session.add(customer)
            db.session.commit()
            return customer
        
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_all_customers() -> list[Customer]:
        """
        Retrieve all customers.

        Returns:
            A list of all customers.
        """
        statement = select(Customer).order_by(
            Customer.first_name,
            Customer.last_name
        )

        return db.session.scalars(statement).all()

    @staticmethod
    def update_customer(
        customer_id: int,
        document_type_id: int | None = None,
        document_number: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> Customer:
        
        """
        Updates an existing customer.

        Args:
            customer_id: Customer identifier.
            document_type_id: New document type ID.
            document_number: New document number.
            first_name: New first name.
            last_name: New last name.
            email: New email address.
            phone: New phone number.

        Returns:
            Customer: The updated customer.

        Raises:
            ValueError: If the customer does not exist, the document type
                does not exist, or the document number/email is already in use.
        """

        customer = CustomerService.get_customer_by_id(customer_id)

        if customer is None:
            raise ValueError("Customer not found")

        #DocumentType
        if document_type_id is not None:

            document_type = db.session.get(
                DocumentType,
                document_type_id
            )

            if document_type is None:
                raise ValueError(
                    "Document type does not exist."
                )

        #Document number
        if (document_number is not None and document_number != customer.document_number):
            customer_with_document = (
                CustomerService.get_customer_by_document(document_number)
            )
            if customer_with_document is not None:
                raise ValueError("Document number already exists")

        #Email
        if (email is not None and email != customer.email):
            customer_with_email = (
                CustomerService.get_customer_by_email(email)
            )
            if customer_with_email is not None:
                raise ValueError("Email already exists.")

        updates = {
            "document_type_id": document_type_id,
            "document_number": document_number,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone
        }
        updates = {
            key: value
            for key, value in updates.items()
            if value is not None
        }
        for field, value in updates.items():
            setattr(customer, field, value)

        try:
            db.session.commit()
            return customer
        except Exception:
            db.session.rollback()
            raise

        