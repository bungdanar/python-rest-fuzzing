from marshmallow import Schema, fields

PRODUCT_FIELDS = ("id", "name", "sku", "regular_price", "discount_price",
                  "quantity", "description", "weight", "note", "published", "seller_id", "created_at", "updated_at")

TAG_FIELDS = ("id", "name", "created_at", "updated_at")

CATEGORY_FIELDS = ("id", "name", "description",
                   "active", "created_at", "updated_at")

COUPON_FIELDS = ("id", "code", "description", "discount_value",
                 "discount_type", "times_used", "max_usage", "start_date", "end_date", "created_at", "updated_at")


class TagResponseSchema(Schema):
    class Meta:
        fields = TAG_FIELDS


class CategoryResponseSchema(Schema):
    class Meta:
        fields = CATEGORY_FIELDS


class CouponResponseSchema(Schema):
    class Meta:
        fields = COUPON_FIELDS


class ProductResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS


class ProductTagCategoryResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS + ("tags", "categories")

    tags = fields.Nested(TagResponseSchema, many=True)
    categories = fields.Nested(CategoryResponseSchema, many=True)


class ProductTagCategoryCouponResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS + ("tags", "categories", "coupons")

    tags = fields.Nested(TagResponseSchema, many=True)
    categories = fields.Nested(CategoryResponseSchema, many=True)
    coupons = fields.Nested(CouponResponseSchema, many=True)


product_res_schema = ProductResponseSchema()

product_tag_category_res_schema = ProductTagCategoryResponseSchema()
product_tag_category_many_res_schema = ProductTagCategoryResponseSchema(
    many=True)

product_tag_category_coupon_res_schema = ProductTagCategoryCouponResponseSchema()
product_tag_category_coupon_many_res_schema = ProductTagCategoryCouponResponseSchema(
    many=True)
