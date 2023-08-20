from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class DateOrDatetimeField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return fields.DateTime()._deserialize(value, attr, data, **kwargs)
        except:
            return fields.Date()._deserialize(value, attr, data, **kwargs)


class CategoryCreatePartialMaValidation(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class CouponCreatePartialMaValidation(Schema):
    code = fields.Str(required=True)
    description = fields.Str(required=True)
    discount_value = fields.Decimal(required=True)
    discount_type = fields.Str(required=True)
    times_used = fields.Int(required=False)
    max_usage = fields.Int(required=True)
    start_date = DateOrDatetimeField(required=True)
    end_date = DateOrDatetimeField(required=True)


class ProductCreatePartialMaValidation(Schema):
    name = fields.Str(required=True)
    sku = fields.Str(required=True)
    regular_price = fields.Decimal(required=True)
    discount_price = fields.Decimal(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str(required=True)
    weight = fields.Decimal(required=True)
    note = fields.Str(required=True)
    published = fields.Boolean(required=False)


class ProductTagCategoryCreatePartialMaValidation(ProductCreatePartialMaValidation):
    tags = fields.List(fields.Str(required=True),
                       required=True, validate=validate.Length(min=1))
    category = fields.Nested(
        CategoryCreatePartialMaValidation(), required=True)


class ProductTagCategoryCouponCreatePartialMaValidation(ProductCreatePartialMaValidation):
    tags = fields.List(fields.Str(required=True),
                       required=True, validate=validate.Length(min=1))

    categories = fields.List(fields.Nested(CategoryCreatePartialMaValidation(
    )), required=True, validate=validate.Length(min=1))

    coupons = fields.List(fields.Nested(CouponCreatePartialMaValidation(
    )), required=True, validate=validate.Length(min=1))


class ProductCreateFullMaValidation(Schema):
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


class CategoryCreateFullMaValidation(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str(required=True, validate=validate.Length(max=1000))


class CouponCreateFullMaValidation(Schema):
    code = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str(required=True, validate=validate.Length(max=1000))
    discount_value = fields.Decimal(required=True, places=2,
                                    validate=validate.Range(min=0, max=100))
    discount_type = fields.Str(
        required=True, validate=validate.Length(max=255))
    times_used = fields.Int(required=False, validate=validate.Range(min=0))
    max_usage = fields.Int(required=True, validate=validate.Range(min=0))
    start_date = DateOrDatetimeField(required=True)
    end_date = DateOrDatetimeField(required=True)

    @validates_schema
    def validate_max_times_used(self, data, **kwargs):
        if 'times_used' in data and data['times_used'] > data['max_usage']:
            raise ValidationError(
                'times_used must be less than or equal to max_usage')

    @validates_schema
    def validate_min_end_data(self, data, **kwargs):
        if data['end_date'] < data['start_date']:
            raise ValidationError(
                'end_date must be greater than or equal to start_date')


class ProductTagCategoryCreateFullMaValidation(ProductCreateFullMaValidation):
    tags = fields.List(fields.Str(required=True, validate=validate.Length(max=255)),
                       required=True, validate=validate.Length(min=1))
    category = fields.Nested(
        CategoryCreateFullMaValidation(), required=True)


class ProductTagCategoryCouponCreateFullMaValidation(ProductCreateFullMaValidation):
    tags = fields.List(fields.Str(required=True, validate=validate.Length(max=255)),
                       required=True, validate=validate.Length(min=1))

    categories = fields.List(fields.Nested(CategoryCreateFullMaValidation(
    )), required=True, validate=validate.Length(min=1))

    coupons = fields.List(fields.Nested(CouponCreateFullMaValidation(
    )), required=True, validate=validate.Length(min=1))
