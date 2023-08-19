from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError as MaValidationError
from pydantic import ValidationError as PydanticValidationError

from common.db import db
from common.handle_validation_err import handle_ma_validation_err, handle_pydantic_validation_err
from common.ma_request_schema import ProductCreateFullMaValidation, ProductCreatePartialMaValidation
from common.pydantic_request_schema import ProductCreatePartialPydanticValidation
from common.response_schema import product_res_schema
from models.product import ProductModel


def _handle_insert_product(data):
    product = ProductModel(**data)
    db.session.add(product)
    db.session.commit()
    return product


def _generate_res_for_created_product(product: ProductModel):
    response = jsonify(product_res_schema.dump(product))
    response.status_code = 201
    return response


class ProductResource(Resource):
    def post(self):
        data = request.get_json()

        product = _handle_insert_product(data)
        return _generate_res_for_created_product(product)


class ProductWithPartialMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductCreatePartialMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        product = _handle_insert_product(validationResult)
        return _generate_res_for_created_product(product)


class ProductWithFullMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductCreateFullMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        product = _handle_insert_product(validationResult)
        return _generate_res_for_created_product(product)


class ProductWithPartialPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductCreatePartialPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        product = _handle_insert_product(validationResult.model_dump())
        return _generate_res_for_created_product(product)
