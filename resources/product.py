from flask import current_app as app
from flask_restful import Resource, reqparse
from ..models.product import Product


class ProductResource(Resource):
    def get(self):
        return {
            "products": []
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("sku")
        parser.add_argument("regular_price")
        parser.add_argument("discount_price")
        parser.add_argument("quantity")
        parser.add_argument("description")
        parser.add_argument("weight")
        parser.add_argument("note")
        parser.add_argument("published")

        data = parser.parse_args()
        product = Product(data)

        try:
            product.save_to_db()
        except Exception as e:
            app.logger.error(e)
            return {
                "message": "Internal Server Error",
                "statusCode": 500
            }, 500

        return product.json(), 201
