from flask_restful import Resource


class ProductResource(Resource):
    def get(self):
        return {
            "products": []
        }

    def post(self):
        return {
            "product": {}
        }, 201
