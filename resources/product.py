from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from common.db import db
from common.schemas import ProductResponseSchema
from models import ProductModel

blp = Blueprint("product", __name__, description="Operation on product")


@blp.route("/api/product")
class Product(MethodView):
    @blp.response(200, ProductResponseSchema(many=True))
    def get(self):
        raise NotImplementedError()

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
