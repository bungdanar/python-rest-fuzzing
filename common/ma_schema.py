from flask_marshmallow import Marshmallow

from models.product import ProductModel
from models.tag import TagModel
from models.category import CategoryModel
from models.coupon import CouponModel
from models.product_tag import ProductTagModel
from models.product_category import ProductCategoryModel
from models.product_coupon import ProductCouponModel

ma = Marshmallow()


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryModel


class CouponSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CouponModel


class ProductTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductTagModel
        include_fk = True


class ProductCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductCategoryModel
        include_fk = True


class ProductCouponSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductCouponModel
        include_fk = True


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

tags_schema = TagSchema(many=True)
categories_schema = CategorySchema(many=True)
coupons_schema = CouponSchema(many=True)
products_tags_schema = ProductTagSchema(many=True)
products_categories_schema = ProductCategorySchema(many=True)
products_coupons_schema = ProductCouponSchema(many=True)
