from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource

from models.category import CategoryModel
from models.product import ProductModel
from models.tag import TagModel
from models.coupon import CouponModel
from common.db import db
from common.response_schema import product_tag_category_coupon_res_schema


class ProductTagCategoryCouponResource(Resource):
    def post(self):
        data = request.get_json()

        tags = itemgetter('tags')(data)
        tags = [{'name': t} for t in tags]
        tags = [TagModel(**t) for t in tags]

        categories = itemgetter('categories')(data)
        categories = [CategoryModel(**c) for c in categories]

        coupons = itemgetter('coupons')(data)
        coupons = [CouponModel(**c) for c in coupons]

        data.pop('tags')
        data.pop('categories')
        data.pop('coupons')

        product = ProductModel(**data)
        product.categories.extend(categories)
        product.tags.extend(tags)
        product.coupons.extend(coupons)

        db.session.add(product)
        db.session.commit()

        res = jsonify(product_tag_category_coupon_res_schema.dump(product))
        res.status_code = 201
        return res
