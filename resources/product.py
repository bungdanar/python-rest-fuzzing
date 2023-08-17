from flask import jsonify, request
from flask_restful import Resource

from common.db import db
from common.ma_schema import product_schema
from models.product import ProductModel


class ProductResource(Resource):
    def post(self):
        data = request.get_json()

        product = ProductModel(**data)

        db.session.add(product)
        db.session.commit()

        res = jsonify(product_schema.dump(product))
        res.status_code = 201
        return res
