from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from common.db import db
from schemas.product import (ProductResponseSchema,
                             ProductCreatePayloadWithMaValidationLv1, ProductCreatePayloadWithMaValidationLv2,
                             ProductQueryWithMaValidationLv1, ProductQueryWithMaValidationLv2)
from models import ProductModel

blp = Blueprint("product", __name__, description="Operation on product")


@blp.route("/api/product")
class Product(MethodView):
    @blp.response(200, ProductResponseSchema(many=True))
    def get(self):
        query = request.args

        try:
            products = ProductModel.query.filter_by(**query)
        except SQLAlchemyError as sql_exc:
            abort(500, message=str(sql_exc))
        except Exception as exc:
            abort(500, message=str(exc))

        return products

    @blp.response(201, ProductResponseSchema)
    def post(self):
        data = request.get_json()

        product = ProductModel(**data)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as sql_exc:
            abort(500, message=str(sql_exc))
        except Exception as exc:
            abort(500, message=str(exc))

        return product


@blp.route("/api/product/ma/lv1")
class ProductWithMaValidationLv1(MethodView):
    @blp.arguments(ProductQueryWithMaValidationLv1, location="query")
    @blp.response(200, ProductResponseSchema(many=True))
    def get(self, args):
        try:
            products = ProductModel.query.filter_by(**args)
        except SQLAlchemyError as sql_exc:
            abort(500, message=str(sql_exc))
        except Exception as exc:
            abort(500, message=str(exc))

        return products

    @blp.arguments(ProductCreatePayloadWithMaValidationLv1)
    @blp.response(201, ProductResponseSchema)
    def post(self, data):
        product = ProductModel(**data)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as sql_exc:
            abort(500, message=str(sql_exc))
        except Exception as exc:
            abort(500, message=str(exc))

        return product


@blp.route("/api/product/ma/lv2")
class ProductWithMaValidationLv2(MethodView):
    @blp.arguments(ProductQueryWithMaValidationLv2, location="query")
    @blp.response(200, ProductResponseSchema(many=True))
    def get(self, args):
        try:
            products = ProductModel.query.filter_by(**args)
        except SQLAlchemyError as sql_exc:
            abort(500, message=str(sql_exc))
        except Exception as exc:
            abort(500, message=str(exc))

        return products

    @blp.arguments(ProductCreatePayloadWithMaValidationLv2)
    @blp.response(201, ProductResponseSchema)
    def post(self, data):
        product = ProductModel(**data)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as sql_exc:
            abort(500, message=str(sql_exc))
        except Exception as exc:
            abort(500, message=str(exc))

        return product
