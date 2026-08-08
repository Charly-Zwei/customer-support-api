from app import create_app
from app.extensions import db
from app.models import DocumentType, Customer, Purchase

app = create_app()

with app.app_context():

    #Document types
    document_type = [
        DocumentType(name="CC"),
        DocumentType(name="TI"),
        DocumentType(name="CE"),
        DocumentType(name="NIT"),
        DocumentType(name="PA"),
        DocumentType(name="PE")
    ]
    db.session.add_all(document_type)
    db.session.flush()

    # Customers
    customers = [
        Customer(
            document_type_id = document_type[0].id,
            document_number = "100000001",
            first_name="Juan",
            last_name="Betancourt",
            email="juan@example.com",
            phone="3001234567"
        ),
        Customer(
            document_type_id=document_type[4].id,
            document_number="100000002",
            first_name="Ana",
            last_name="Gomez",
            email="ana@example.com",
            phone="3007654321"
        ),
        Customer(
            document_type_id=document_type[2].id,
            document_number="100000003",
            first_name="Pedro",
            last_name="Martinez",
            email="pedro@example.com",
            phone="3015555555"
        )
    ]

    db.session.add_all(customers)
    db.session.flush()

    # Purchases
    purchases = [
        Purchase(
            customer_id=customers[0].id,
            amount=2_000_000,
            description="Purchase 1"
        ),
        Purchase(
            customer_id=customers[0].id,
            amount=1_500_000,
            description="Purchase 2"
        ),
        Purchase(
            customer_id=customers[0].id,
            amount=2_000_000,
            description="Purchase 3"
        ),
        Purchase(
            customer_id=customers[1].id,
            amount=1_000_000,
            description="Purchase 1"
        ),
        Purchase(
            customer_id=customers[1].id,
            amount=500_000,
            description="Purchase 2"
        ),
        Purchase(
            customer_id=customers[2].id,
            amount=4_000_000,
            description="Purchase 1"
        )
    ]

    db.session.add_all(purchases)
    db.session.commit()

    print("Database seeded.")