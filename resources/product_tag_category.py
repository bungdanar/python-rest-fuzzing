from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource, abort
from marshmallow import ValidationError as MaValidationError
from pydantic import ValidationError as PydanticValidationError
from common.handle_validation_err import handle_ma_validation_err, handle_pydantic_validation_err
from common.ma_request_schema import ProductTagCategoryCreateFullMaValidation, ProductTagCategoryCreatePartialMaValidation
from common.pydantic_request_schema import ProductTagCategoryCreateFullPydanticValidation, ProductTagCategoryCreatePartialPydanticValidation

from models.category import CategoryModel
from models.product import ProductModel
from models.tag import TagModel
from common.db import db
from common.response_schema import product_tag_category_res_schema


def _handle_insert_product(data):
    tags = itemgetter('tags')(data)
    tags = [{'name': t} for t in tags]
    tags = [TagModel(**t) for t in tags]

    category = itemgetter('category')(data)
    category = CategoryModel(**category)

    data.pop('tags')
    data.pop('category')

    product = ProductModel(**data)
    product.categories.append(category)
    product.tags.extend(tags)

    db.session.add(product)
    db.session.commit()

    return product


def _generate_res_for_created_product(product: ProductModel):
    response = jsonify(product_tag_category_res_schema.dump(product))
    response.status_code = 201
    return response


class ProductTagCategoryResource(Resource):
    def post(self):
        data = request.get_json()

        product = _handle_insert_product(data)
        return _generate_res_for_created_product(product)


class ProductTagCategoryWithPartialMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCreatePartialMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        product = _handle_insert_product(validationResult)
        return _generate_res_for_created_product(product)


class ProductTagCategoryWithFullMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCreateFullMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        product = _handle_insert_product(validationResult)
        return _generate_res_for_created_product(product)


class ProductTagCategoryWithPartialPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCreatePartialPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        product = _handle_insert_product(validationResult.model_dump())
        return _generate_res_for_created_product(product)


class ProductTagCategoryWithFullPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = ProductTagCategoryCreateFullPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        product = _handle_insert_product(validationResult.model_dump())
        return _generate_res_for_created_product(product)
