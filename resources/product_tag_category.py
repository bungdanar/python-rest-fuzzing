from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource
from models.category import CategoryModel

from models.product import ProductModel
from common.db import db
from common.response_schema import product_tag_category_res_schema
from models.tag import TagModel


class ProductTagCategoryResource(Resource):
    def post(self):
        data = request.get_json()

        tags = itemgetter('tags')(data)
        tags = [{'name': t} for t in tags]
        category = itemgetter('category')(data)

        data.pop('tags')
        data.pop('category')

        created_product = ProductModel(**data)
        created_category = CategoryModel(**category)
        created_tags = [TagModel(**t) for t in tags]

        created_product.categories.append(created_category)
        created_product.tags.extend(created_tags)

        db.session.add(created_product)
        db.session.commit()

        res = jsonify(product_tag_category_res_schema.dump(created_product))
        res.status_code = 201
        return res
