from datetime import datetime

from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class DateOrDatetimeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            # Try parsing as datetime first
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
        except ValueError:
            try:
                # Try parsing as date
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date/datetime format")


class CategoryCreatePartialValidation(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class CouponCreatePartialValidation(Schema):
    code = fields.Str(required=True)
    description = fields.Str(required=True)
    discount_value = fields.Decimal(required=True)
    discount_type = fields.Str(required=True)
    times_used = fields.Int(required=False)
    max_usage = fields.Int(required=True)
    start_date = DateOrDatetimeField(required=True)
    end_date = DateOrDatetimeField(required=True)


class ProductCreatePartialValidation(Schema):
    name = fields.Str(required=True)
    sku = fields.Str(required=True)
    regular_price = fields.Decimal(required=True)
    discount_price = fields.Decimal(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str(required=True)
    weight = fields.Decimal(required=True)
    note = fields.Str(required=True)
    published = fields.Boolean(required=False)


class ProductTagCategoryCreatePartialValidation(ProductCreatePartialValidation):
    tags = fields.List(fields.Str(required=True),
                       required=True, validate=validate.Length(min=1))
    category = fields.Nested(
        CategoryCreatePartialValidation(), required=True)


class ProductTagCategoryCouponCreatePartialValidation(ProductCreatePartialValidation):
    tags = fields.List(fields.Str(required=True),
                       required=True, validate=validate.Length(min=1))

    categories = fields.List(fields.Nested(CategoryCreatePartialValidation(
    )), required=True, validate=validate.Length(min=1))

    coupons = fields.List(fields.Nested(CouponCreatePartialValidation(
    )), required=True, validate=validate.Length(min=1))


class ProductCreateFullValidation(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    sku = fields.Str(required=True, validate=validate.Length(max=255))
    regular_price = fields.Decimal(
        required=True, places=4, validate=validate.Range(min=0))
    discount_price = fields.Decimal(
        required=True, places=4, validate=validate.Range(min=0))
    quantity = fields.Int(
        required=True, validate=validate.Range(min=0, max=9999))
    description = fields.Str(
        required=True, validate=validate.Length(max=1000))
    weight = fields.Decimal(required=True, places=4,
                            validate=validate.Range(min=0, max=1000))
    note = fields.Str(required=True, validate=validate.Length(max=255))
    published = fields.Boolean(required=False)

    @validates_schema
    def validate_max_discount_price(self, data, **kwargs):
        if data['discount_price'] > data['regular_price']:
            raise ValidationError(
                'discount_price must be less than or equal to regular_price')


class CategoryCreateFullValidation(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str(required=True, validate=validate.Length(max=1000))


class ProductTagCategoryCreateFullValidation(ProductCreateFullValidation):
    tags = fields.List(fields.Str(required=True, validate=validate.Length(max=255)),
                       required=True, validate=validate.Length(min=1))
    category = fields.Nested(
        CategoryCreateFullValidation(), required=True)
