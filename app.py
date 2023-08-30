import os
import time

from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from common.custom_logger import create_res_time_logger
from common.db import db
from common.ma import ma
from resources.product import (
    ProductResource,
    ProductWithFullMaValidationResource,
    ProductWithFullPydanticValidationResource,
    ProductWithPartialMaValidationResource,
    ProductWithPartialPydanticValidationResource
)
from resources.product_tag_category import (
    ProductTagCategoryResource,
    ProductTagCategoryWithFullMaValidationResource,
    ProductTagCategoryWithFullPydanticValidationResource,
    ProductTagCategoryWithPartialMaValidationResource,
    ProductTagCategoryWithPartialPydanticValidationResource
)
from resources.product_tag_category_coupon import (
    ProductTagCategoryCouponResource,
    ProductTagCategoryCouponWithFullMaValidationResource,
    ProductTagCategoryCouponWithFullPydanticValidationResource,
    ProductTagCategoryCouponWithPartialMaValidationResource,
    ProductTagCategoryCouponWithPartialPydanticValidationResource
)
from resources.test import Test
import models
from resources.user import (
    UserFullMaValidationResource,
    UserPartialMaValidationResource,
    UserResource
)
from resources.user_addr_prod import (
    UserAddrProdFullMaValidationResource,
    UserAddrProdPartialMaValidationResource,
    UserAddrProdResource
)
from resources.user_addr_prod_ship import (
    UserAddrProdShipFullMaValidationResource,
    UserAddrProdShipPartialMaValidationResource,
    UserAddrProdShipResource
)
from resources.user_address import (
    UserAddressFullMaValidationResource,
    UserAddressPartialMaValidationResource,
    UserAddressResource
)


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    ma.init_app(app)
    api = Api(app)

    VALIDATION_MODE = os.getenv("VALIDATION", "no")

    res_time_logger = create_res_time_logger()

    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_response_time(response):
        if hasattr(request, 'start_time'):
            res_time = (time.time() - request.start_time) * 1000
            res_time_logger.info(
                f' {request.method} {request.path} {response.status_code} {res_time:.3f}ms validation={VALIDATION_MODE}')

        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e

        print('EXCEPTION: ', e)

        return jsonify({
            "statusCode": 500,
            "message": "Internal Server Error"
        }), 500

    api.add_resource(Test, '/')

    if VALIDATION_MODE == 'ma-partial':
        api.add_resource(
            ProductWithPartialMaValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithPartialMaValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithPartialMaValidationResource,
                         '/api/product-tag-category-coupon')

        api.add_resource(UserPartialMaValidationResource, '/api/user')
        api.add_resource(
            UserAddressPartialMaValidationResource, '/api/user-address')
        api.add_resource(UserAddrProdPartialMaValidationResource,
                         '/api/user-address-product')
        api.add_resource(UserAddrProdShipPartialMaValidationResource,
                         '/api/user-address-product-shipping')

    elif VALIDATION_MODE == 'ma-full':
        api.add_resource(ProductWithFullMaValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithFullMaValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithFullMaValidationResource,
                         '/api/product-tag-category-coupon')

        api.add_resource(UserFullMaValidationResource, '/api/user')
        api.add_resource(
            UserAddressFullMaValidationResource, '/api/user-address')
        api.add_resource(UserAddrProdFullMaValidationResource,
                         '/api/user-address-product')
        api.add_resource(UserAddrProdShipFullMaValidationResource,
                         '/api/user-address-product-shipping')

    elif VALIDATION_MODE == 'pydantic-partial':
        api.add_resource(
            ProductWithPartialPydanticValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithPartialPydanticValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithPartialPydanticValidationResource,
                         '/api/product-tag-category-coupon')

    elif VALIDATION_MODE == 'pydantic-full':
        api.add_resource(
            ProductWithFullPydanticValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithFullPydanticValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithFullPydanticValidationResource,
                         '/api/product-tag-category-coupon')

    else:
        api.add_resource(ProductResource, '/api/product')
        api.add_resource(ProductTagCategoryResource,
                         '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponResource,
                         '/api/product-tag-category-coupon')

        api.add_resource(UserResource, '/api/user')
        api.add_resource(UserAddressResource, '/api/user-address')
        api.add_resource(UserAddrProdResource, '/api/user-address-product')
        api.add_resource(UserAddrProdShipResource,
                         '/api/user-address-product-shipping')

        VALIDATION_MODE = 'no'

    app.logger.info(f"App is running with validation mode: {VALIDATION_MODE}")

    return app
