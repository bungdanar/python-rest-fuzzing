import os
import time
import logging
import sys

from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from common.custom_logger import create_res_time_logger, create_err_500_logger
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
    UserResource,
    UserFullPydanticValidationResource,
    UserPartialPydanticValidationResource
)
from resources.user_addr_prod import (
    UserAddrProdFullMaValidationResource,
    UserAddrProdFullPydanticValidationResource,
    UserAddrProdPartialMaValidationResource,
    UserAddrProdPartialPydanticValidationResource,
    UserAddrProdResource
)
from resources.user_addr_prod_ship import (
    UserAddrProdShipFullMaValidationResource,
    UserAddrProdShipFullPydanticValidationResource,
    UserAddrProdShipPartialMaValidationResource,
    UserAddrProdShipPartialPydanticValidationResource,
    UserAddrProdShipResource
)
from resources.user_address import (
    UserAddrFullPydanticValidationResource,
    UserAddrPartialPydanticValidationResource,
    UserAddressFullMaValidationResource,
    UserAddressPartialMaValidationResource,
    UserAddressResource
)


def create_app(db_url=None):
    app = Flask(__name__)

    if not app.debug:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    ma.init_app(app)
    api = Api(app)

    # Check db connection
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            app.logger.info('Connected to database')
        except Exception as e:
            dbErr = str(e)
            sys.exit(dbErr)

    VALIDATION_MODE = os.getenv("VALIDATION", "no")

    res_time_logger = create_res_time_logger()
    err_500_logger = create_err_500_logger()

    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_response_time(response):
        if hasattr(request, 'start_time'):
            res_time = (time.time() - request.start_time) * 1000
            res_time_logger.info(
                f'{request.method} {request.path} {response.status_code} {res_time:.3f}ms validation={VALIDATION_MODE}')

        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e

        print('EXCEPTION: ', e)

        status_code = 500

        err_msg = str(e)
        if isinstance(e, SQLAlchemyError):
            err_msg = err_msg.split('\n')[0]

        err_500_logger.info(
            f'#{request.method}#{request.path}#{status_code}#validation={VALIDATION_MODE}#msg={err_msg}'
        )

        return jsonify({
            "statusCode": status_code,
            "message": err_msg
        }), status_code

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

        api.add_resource(
            UserPartialPydanticValidationResource, '/api/user')
        api.add_resource(
            UserAddrPartialPydanticValidationResource, '/api/user-address')
        api.add_resource(
            UserAddrProdPartialPydanticValidationResource, '/api/user-address-product')
        api.add_resource(UserAddrProdShipPartialPydanticValidationResource,
                         '/api/user-address-product-shipping')

    elif VALIDATION_MODE == 'pydantic-full':
        api.add_resource(
            ProductWithFullPydanticValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithFullPydanticValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithFullPydanticValidationResource,
                         '/api/product-tag-category-coupon')

        api.add_resource(
            UserFullPydanticValidationResource, '/api/user')
        api.add_resource(
            UserAddrFullPydanticValidationResource, '/api/user-address')
        api.add_resource(
            UserAddrProdFullPydanticValidationResource, '/api/user-address-product')
        api.add_resource(UserAddrProdShipFullPydanticValidationResource,
                         '/api/user-address-product-shipping')

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
