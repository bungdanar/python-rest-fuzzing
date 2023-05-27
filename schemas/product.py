from marshmallow import Schema, fields


class ProductResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    sku = fields.Str()
    regular_price = fields.Decimal()
    discount_price = fields.Decimal()
    quantity = fields.Int()
    description = fields.Str()
    weight = fields.Float()
    note = fields.Str()
    published = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
