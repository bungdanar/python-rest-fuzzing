from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError as MaValidationError
from pydantic import ValidationError as PydanticValidationError

from models.user import UserModel
from models.role import RoleModel
from models.address import AddressModel
from models.product import ProductModel
from common.db import db
from common.response_schema import user_addr_prod_res_schema
from common.ma_request_schema import UserAddrProdCreateFullMaValidation, UserAddrProdCreatePartialMaValidation
from common.pydantic_request_schema import UserAddrProdCreateFullPydanticValidation, UserAddrProdCreatePartialPydanticValidation
from common.handle_validation_err import handle_ma_validation_err, handle_pydantic_validation_err


def _handle_insert_user(data):
    addresses = itemgetter('addresses')(data)
    addresses = [AddressModel(**a) for a in addresses]

    product = itemgetter('product')(data)
    product = ProductModel(**product)

    role = RoleModel.query.get(2)

    data.pop('addresses')
    data.pop('product')

    user = UserModel(**data)
    user.roles.append(role)
    user.addresses.extend(addresses)
    user.products.append(product)

    db.session.add(user)
    db.session.commit()

    return user


def _generate_res_for_created_user(user: UserModel):
    response = jsonify(user_addr_prod_res_schema.dump(user))
    response.status_code = 201
    return response


class UserAddrProdResource(Resource):
    def post(self):
        data = request.get_json()

        user = _handle_insert_user(data)
        return _generate_res_for_created_user(user)


class UserAddrProdPartialMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrProdCreatePartialMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        user = _handle_insert_user(validationResult)
        return _generate_res_for_created_user(user)


class UserAddrProdFullMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrProdCreateFullMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        user = _handle_insert_user(validationResult)
        return _generate_res_for_created_user(user)


class UserAddrProdPartialPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrProdCreatePartialPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        user = _handle_insert_user(validationResult.model_dump())
        return _generate_res_for_created_user(user)


class UserAddrProdFullPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrProdCreateFullPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        user = _handle_insert_user(validationResult.model_dump())
        return _generate_res_for_created_user(user)
