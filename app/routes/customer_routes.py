from flask import Blueprint, request
from marshmallow import ValidationError
from app.schemas.customer_schema import customer_schema, customers_schema
from app.services.customer_services import CustomerService

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.post("")
def create_customer():
    try:
        data = customer_schema.load(request.get_json())

        customer = CustomerService.create_customer(**data)

        return customer_schema.dump(customer), 201
    except ValidationError as error:
        return {"message": error.messages}, 400
    except ValueError as error:
        return {"message": str(error)}, 400


@customer_bp.get("/<string:document_number>")
def get_customer(document_number):
    customer = CustomerService.get_customer_by_document(document_number)
    if customer is None:
        return {"message": "Customer not found"}, 404

    return customer_schema.dump(customer), 200

@customer_bp.get("")
def get_all_customers():
    customers = CustomerService.get_all_customers()

    return customers_schema.dump(customers), 200

@customer_bp.put("/<int:customer_id>")
def update_customer(customer_id):
    try:
        data = customer_schema.load(request.get_json(), partial=True)

        customer = CustomerService.update_customer(customer_id, **data)
        return customer_schema.dump(customer), 200
    except ValidationError as error:
        return {"message": error.messages}, 400
    except ValueError as error:
        return {"message": str(error)}, 400