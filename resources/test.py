from flask import jsonify
from flask_restful import Resource

from common.ma_schema import products_schema
from common.ma_schema import tags_schema
from common.ma_schema import categories_schema
from common.ma_schema import coupons_schema
from common.ma_schema import products_tags_schema
from common.ma_schema import products_categories_schema
from common.ma_schema import products_coupons_schema
from models.product import ProductModel
from models.tag import TagModel
from models.category import CategoryModel
from models.coupon import CouponModel
from models.product_tag import ProductTagModel
from models.product_category import ProductCategoryModel
from models.product_coupon import ProductCouponModel


class Test(Resource):
    def get(self):
        # products = ProductModel.query.limit(10).all()
        # result = products_schema.dump(products)
        # return jsonify(result)

        # tags = TagModel.query.limit(10).all()
        # result = tags_schema.dump(tags)
        # return jsonify(result)

        # categories = CategoryModel.query.limit(10).all()
        # result = categories_schema.dump(categories)
        # return jsonify(result)

        # coupons = CouponModel.query.limit(10).all()
        # result = coupons_schema.dump(coupons)
        # return jsonify(result)

        # products_tags = ProductTagModel.query.limit(10).all()
        # result = products_tags_schema.dump(products_tags)
        # return jsonify(result)

        # products_categories = ProductCategoryModel.query.limit(10).all()
        # result = products_categories_schema.dump(products_categories)
        # return jsonify(result)

        products_coupons = ProductCouponModel.query.limit(10).all()
        result = products_coupons_schema.dump(products_coupons)
        return jsonify(result)
