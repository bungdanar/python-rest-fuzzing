from marshmallow import Schema, fields


class ProductCreatePayloadWithPartialValidation(Schema):
    name = fields.Str(required=True)
    sku = fields.Str(required=True)
    regular_price = fields.Decimal(required=True)
    discount_price = fields.Decimal(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str(required=True)
    weight = fields.Float(required=True)
    note = fields.Str(required=True)
    published = fields.Boolean(required=False)
