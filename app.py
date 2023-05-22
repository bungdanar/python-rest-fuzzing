from os import environ
from flask import Flask
from flask_restful import Api
from .resources.product import ProductResource
from .common.db import db, migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS")

api = Api(app)


@app.route("/")
def hello_world():
    return "<p>Hello World</p>"


api.add_resource(ProductResource, "/api/product")

db.init_app(app)
migrate.init_app(app, db)
