from marshmallow import Schema, fields, validate


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


class ProductQueryWithMaValidationLv1(Schema):
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


class ProductQueryWithMaValidationLv2(Schema):
    id = fields.Int()
    name = fields.Str(validate=validate.Length(min=1, max=255))
    sku = fields.Str(validate=validate.Length(min=1, max=255))
    regular_price = fields.Decimal(validate=validate.Range(min=0))
    discount_price = fields.Decimal(validate=validate.Range(min=0))
    quantity = fields.Int(validate=validate.Range(min=0))
    description = fields.Str(validate=validate.Length(min=1, max=1000))
    weight = fields.Float(validate=validate.Range(min=0))
    note = fields.Str(validate=validate.Length(min=1, max=255))
    published = fields.Boolean()
    created_at = fields.DateTime()


class ProductCreatePayloadWithMaValidationLv1(Schema):
    name = fields.Str(required=True)
    sku = fields.Str(required=True)
    regular_price = fields.Decimal(required=True)
    discount_price = fields.Decimal(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str(required=True)
    weight = fields.Float(required=True)
    note = fields.Str(required=True)
    published = fields.Boolean(required=False)


class ProductCreatePayloadWithMaValidationLv2(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    regular_price = fields.Decimal(
        required=True, places=4, validate=validate.Range(min=0))
    discount_price = fields.Decimal(
        required=True, places=4, validate=validate.Range(min=0))
    quantity = fields.Int(required=True, validate=validate.Range(min=0))
    description = fields.Str(
        required=True, validate=validate.Length(min=3, max=1000))
    weight = fields.Float(required=True, validate=validate.Range(min=0))
    note = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    published = fields.Boolean(required=False)
