from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError as MaValidationError
from pydantic import ValidationError as PydanticValidationError
from common.handle_validation_err import handle_ma_validation_err, handle_pydantic_validation_err
from common.ma_request_schema import ProductTagCategoryCouponCreateFullMaValidation, ProductTagCategoryCouponCreatePartialMaValidation
from common.pydantic_request_schema import ProductTagCategoryCouponCreateFullPydanticValidation, ProductTagCategoryCouponCreatePartialPydanticValidation

from models.category import CategoryModel
from models.product import ProductModel
from models.tag import TagModel
from models.coupon import CouponModel
from common.db import db
from common.response_schema import product_tag_category_coupon_res_schema


def _handle_insert_product(data):
    tags = itemgetter('tags')(data)
    tags = [{'name': t} for t in tags]
    tags = [TagModel(**t) for t in tags]

    categories = itemgetter('categories')(data)
    categories = [CategoryModel(**c) for c in categories]

    coupons = itemgetter('coupons')(data)
    coupons = [CouponModel(**c) for c in coupons]

    data.pop('tags')
    data.pop('categories')
    data.pop('coupons')

    product = ProductModel(**data)
    product.categories.extend(categories)
    product.tags.extend(tags)
    product.coupons.extend(coupons)

    db.session.add(product)
    db.session.commit()

    return product


def _generate_res_for_created_product(product: ProductModel):
    response = jsonify(product_tag_category_coupon_res_schema.dump(product))
    response.status_code = 201
    return response


class ProductTagCategoryCouponResource(Resource):
    def post(self):
        data = request.get_json()

        product = _handle_insert_product(data)
        return _generate_res_for_created_product(product)


class ProductTagCategoryCouponWithPartialMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCouponCreatePartialMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        product = _handle_insert_product(validationResult)
        return _generate_res_for_created_product(product)


class ProductTagCategoryCouponWithFullMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCouponCreateFullMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        product = _handle_insert_product(validationResult)
        return _generate_res_for_created_product(product)


class ProductTagCategoryCouponWithPartialPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCouponCreatePartialPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        product = _handle_insert_product(validationResult.model_dump())
        return _generate_res_for_created_product(product)


class ProductTagCategoryCouponWithFullPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCouponCreateFullPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        product = _handle_insert_product(validationResult.model_dump())
        return _generate_res_for_created_product(product)
