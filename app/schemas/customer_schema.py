from marshmallow import Schema, fields
from app.schemas.document_schema import DocumentTypeSchema


class CustomerSchema(Schema):
    """
    Customer serialization and validation schema.
    """

    id = fields.Int(dump_only=True)

    #document_type_id = fields.Int(required=True)
    document_type = fields.Function(
        serialize=lambda customer: customer.document_type.name,
        deserialize=lambda value: value,
        required=True
    )
    
    document_number = fields.Str(required=True)

    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    email = fields.Email(required=True)
    phone = fields.Str(required=True)

    created_at = fields.DateTime(dump_only=True)


#Instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)