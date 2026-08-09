from marshmallow import Schema, fields

class PurchaseSchema(Schema):
    """
    Purchase serialization and validation schema
    """

    id = fields.Int(dump_only=True)

    customer_id = fields.Int(required=True)

    amount = fields.Decimal(required=True)

    description = fields.Str()
    
    purchase_date = fields.DateTime(dump_only=True)


#Instances
purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)