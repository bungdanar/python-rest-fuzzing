from flask import Flask
from flask_restful import Api
from .resources.product import ProductResource

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello_world():
    return "<p>Hello World</p>"


api.add_resource(ProductResource, "/api/product")
