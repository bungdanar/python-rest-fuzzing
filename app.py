import os

from flask import Flask
from flask_restful import Api

from common.db import db
from common.ma import ma
from resources.product import ProductResource, ProductWithFullMaValidationResource, ProductWithFullPydanticValidationResource, ProductWithPartialMaValidationResource, ProductWithPartialPydanticValidationResource
from resources.product_tag_category import ProductTagCategoryResource, ProductTagCategoryWithFullMaValidationResource, ProductTagCategoryWithFullPydanticValidationResource, ProductTagCategoryWithPartialMaValidationResource, ProductTagCategoryWithPartialPydanticValidationResource
from resources.product_tag_category_coupon import ProductTagCategoryCouponResource, ProductTagCategoryCouponWithFullMaValidationResource, ProductTagCategoryCouponWithFullPydanticValidationResource, ProductTagCategoryCouponWithPartialMaValidationResource, ProductTagCategoryCouponWithPartialPydanticValidationResource
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

    VALIDATION_MODE = os.getenv("VALIDATION", "no")

    api.add_resource(Test, '/')

    if VALIDATION_MODE == 'ma-partial':
        api.add_resource(
            ProductWithPartialMaValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithPartialMaValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithPartialMaValidationResource,
                         '/api/product-tag-category-coupon')

    elif VALIDATION_MODE == 'ma-full':
        api.add_resource(ProductWithFullMaValidationResource, '/api/product')
        api.add_resource(
            ProductTagCategoryWithFullMaValidationResource, '/api/product-tag-category')
        api.add_resource(ProductTagCategoryCouponWithFullMaValidationResource,
                         '/api/product-tag-category-coupon')

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

        VALIDATION_MODE = 'no'

    app.logger.info(f"App is running with validation mode: {VALIDATION_MODE}")

    return app
