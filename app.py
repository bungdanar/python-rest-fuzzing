import os

from flask import Flask
from flask_restful import Api

from common.db import db
from common.ma import ma
from resources.product import ProductResource
from resources.test import Test
import models


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    ma.init_app(app)
    api = Api(app)

    api.add_resource(Test, '/')
    api.add_resource(ProductResource, '/api/product')

    return app
