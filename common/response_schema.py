from marshmallow import Schema, fields

PRODUCT_FIELDS = ("id", "name", "sku", "regular_price", "discount_price",
                  "quantity", "description", "weight", "note", "published", "seller_id", "created_at", "updated_at")

TAG_FIELDS = ("id", "name", "created_at", "updated_at")

CATEGORY_FIELDS = ("id", "name", "description",
                   "active", "created_at", "updated_at")

COUPON_FIELDS = ("id", "code", "description", "discount_value",
                 "discount_type", "times_used", "max_usage", "start_date", "end_date", "created_at", "updated_at")

USER_FIELDS = ("id", "first_name", "last_name", "email",
               "phone_code", "phone_number", "created_at", "updated_at")

ADDRESS_FIELDS = ("id", "street", "city", "country",
                  "postal_code", "user_id", "created_at", "updated_at")

SHIPPING_FIELDS = ("id", "description", "charge", "free",
                   "estimated_days", "product_id", "created_at", "updated_at")


class TagResponseSchema(Schema):
    class Meta:
        fields = TAG_FIELDS


class CategoryResponseSchema(Schema):
    class Meta:
        fields = CATEGORY_FIELDS


class CouponResponseSchema(Schema):
    class Meta:
        fields = COUPON_FIELDS


class ShippingResponseSchema(Schema):
    class Meta:
        fields = SHIPPING_FIELDS


class ProductResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS


class ProductShippingResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS + ("shippings",)

    shippings = fields.Nested(ShippingResponseSchema, many=True)


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


class UserResponseSchema(Schema):
    class Meta:
        fields = USER_FIELDS


class AddressResponseSchema(Schema):
    class Meta:
        fields = ADDRESS_FIELDS


class UserAddrResSchema(Schema):
    class Meta:
        fields = USER_FIELDS + ('addresses',)

    addresses = fields.Nested(AddressResponseSchema, many=True)


class UserAddrProdResSchema(Schema):
    class Meta:
        fields = USER_FIELDS + ('addresses', 'products')

    addresses = fields.Nested(AddressResponseSchema, many=True)
    products = fields.Nested(ProductResponseSchema, many=True)


class UserAddrProdShipResSchema(Schema):
    class Meta:
        fields = USER_FIELDS + ('addresses', 'products')

    addresses = fields.Nested(AddressResponseSchema, many=True)
    products = fields.Nested(ProductShippingResponseSchema, many=True)


product_res_schema = ProductResponseSchema()

product_tag_category_res_schema = ProductTagCategoryResponseSchema()
product_tag_category_many_res_schema = ProductTagCategoryResponseSchema(
    many=True)

product_tag_category_coupon_res_schema = ProductTagCategoryCouponResponseSchema()
product_tag_category_coupon_many_res_schema = ProductTagCategoryCouponResponseSchema(
    many=True)

user_res_schema = UserResponseSchema()
user_addr_res_schema = UserAddrResSchema()
user_addr_prod_res_schema = UserAddrProdResSchema()
user_addr_prod_ship_res_schema = UserAddrProdShipResSchema()
