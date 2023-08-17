from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource

from models.category import CategoryModel
from models.product import ProductModel
from models.tag import TagModel
from common.db import db
from common.response_schema import product_tag_category_res_schema


class ProductTagCategoryResource(Resource):
    def post(self):
        data = request.get_json()

        tags = itemgetter('tags')(data)
        tags = [{'name': t} for t in tags]
        tags = [TagModel(**t) for t in tags]

        category = itemgetter('category')(data)
        category = CategoryModel(**category)

        data.pop('tags')
        data.pop('category')

        product = ProductModel(**data)
        product.categories.append(category)
        product.tags.extend(tags)

        db.session.add(product)
        db.session.commit()

        res = jsonify(product_tag_category_res_schema.dump(product))
        res.status_code = 201
        return res
