from flask import jsonify, request
from flask_restful import Resource


class ProductTagCategoryResource(Resource):
    def post(self):
        data = request.get_json()
