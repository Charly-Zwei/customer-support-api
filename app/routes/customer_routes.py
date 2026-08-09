from flask import Blueprint, request, send_file
from marshmallow import ValidationError
from app.schemas.customer_schema import customer_schema, customers_schema
from app.schemas.purchase_schema import purchases_schema
from app.services.customer_services import CustomerService
from app.services.purchase_service import PurchaseService
from app.services.export_service import ExportService
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


@customer_bp.get("/<string:document_type>/<string:document_number>")
def get_customer(document_type, document_number):
    customer = CustomerService.get_customer_by_document(document_type, document_number)
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

@customer_bp.get("/<int:customer_id>/purchases")
def get_customer_purchases(customer_id):
    try:
        purchases = PurchaseService.get_customer_purchases(
            customer_id
        )

        return purchases_schema.dump(purchases), 200

    except ValueError as error:
        return {"message": str(error)}, 404

@customer_bp.get("/<int:customer_id>/export")
def export_customer(customer_id):
    customer = CustomerService.get_customer_by_id(customer_id)
    if customer is None:
        return {"message": "Customer not found"}, 404

    output = ExportService.customer_excel(customer)

    return send_file(
        output,
        as_attachment=True,
        download_name=f"customer_{customer.id}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )