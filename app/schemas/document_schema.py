from marshmallow import Schema, fields


class DocumentTypeSchema(Schema):
    """
    Document type serialization schema.
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


# Instances
document_type_schema = DocumentTypeSchema()
document_types_schema = DocumentTypeSchema(many=True)