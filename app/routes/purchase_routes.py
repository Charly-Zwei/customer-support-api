from flask import Blueprint, request
from marshmallow import ValidationError
from app.schemas.purchase_schema import purchase_schema, purchases_schema
from app.services.purchase_service import PurchaseService

purchase_bp = Blueprint("purchases", __name__, url_prefix="/purchases")

@purchase_bp.post("")
def create_purchase():
    try:
        data = purchase_schema.load(request.get_json())

        purchase = PurchaseService.create_purchase(**data)

        return purchase_schema.dump(purchase), 201
    except ValidationError as error:
        return {"message": error.messages}, 400
    except ValueError as error:
        return {"message": str(error)}, 400

@purchase_bp.get("/<int:purchase_id>")
def get_purchase(purchase_id):
    purchase = PurchaseService.get_purchase_by_id(purchase_id)

    if purchase is None:
        return {"message": "Purchase not found"}, 404

    return purchase_schema.dump(purchase), 200

@purchase_bp.get("")
def get_all_purchases():
    purchases = PurchaseService.get_all_purchases()

    return purchases_schema.dump(purchases), 200