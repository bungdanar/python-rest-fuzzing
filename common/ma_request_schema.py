from marshmallow import Schema, fields, validate


class CategoryCreatePayloadWithPartialValidation(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)


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


class ProductTagCategoryCreatePayloadWithPartialValidation(ProductCreatePayloadWithPartialValidation):
    tags = fields.List(fields.Str(required=True),
                       required=True, validate=validate.Length(min=1))
    category = fields.Nested(
        CategoryCreatePayloadWithPartialValidation(), required=True)
