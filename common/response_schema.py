from marshmallow import Schema, fields

PRODUCT_FIELDS = ("id", "name", "sku", "regular_price", "discount_price",
                  "quantity", "description", "weight", "note", "published", "created_at", "updated_at")

TAG_FIELDS = ("id", "name", "created_at", "updated_at")

CATEGORY_FIELDS = ("id", "name", "description",
                   "active", "created_at", "updated_at")


class TagResponseSchema(Schema):
    class Meta:
        fields = TAG_FIELDS


class CategoryResponseSchema(Schema):
    class Meta:
        fields = CATEGORY_FIELDS


class ProductResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS


class ProductTagCategoryResponseSchema(Schema):
    class Meta:
        fields = PRODUCT_FIELDS + ("tags", "categories")

    tags = fields.Nested(TagResponseSchema, many=True)
    categories = fields.Nested(CategoryResponseSchema, many=True)


product_res_schema = ProductResponseSchema()

product_tag_category_res_schema = ProductTagCategoryResponseSchema()
product_tag_category_many_res_schema = ProductTagCategoryResponseSchema(
    many=True)
