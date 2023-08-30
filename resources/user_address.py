from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError as MaValidationError
from pydantic import ValidationError as PydanticValidationError

from models.user import UserModel
from models.role import RoleModel
from models.address import AddressModel
from common.db import db
from common.response_schema import user_addr_res_schema
from common.ma_request_schema import UserAddrCreateFullMaValidation, UserAddrCreatePartialMaValidation
from common.pydantic_request_schema import UserAddrCreateFullPydanticValidation, UserAddrCreatePartialPydanticValidation
from common.handle_validation_err import handle_ma_validation_err, handle_pydantic_validation_err


def _handle_insert_user(data):
    address = itemgetter('address')(data)
    address = AddressModel(**address)

    role = RoleModel.query.get(2)

    data.pop('address')

    user = UserModel(**data)
    user.roles.append(role)
    user.addresses.append(address)

    db.session.add(user)
    db.session.commit()

    return user


def _generate_res_for_created_user(user: UserModel):
    response = jsonify(user_addr_res_schema.dump(user))
    response.status_code = 201
    return response


class UserAddressResource(Resource):
    def post(self):
        data = request.get_json()

        user = _handle_insert_user(data)
        return _generate_res_for_created_user(user)


class UserAddressPartialMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrCreatePartialMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        user = _handle_insert_user(validationResult)
        return _generate_res_for_created_user(user)


class UserAddressFullMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrCreateFullMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        user = _handle_insert_user(validationResult)
        return _generate_res_for_created_user(user)


class UserAddrPartialPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrCreatePartialPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        user = _handle_insert_user(validationResult.model_dump())
        return _generate_res_for_created_user(user)


class UserAddrFullPydanticValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrCreateFullPydanticValidation.model_validate(
                data, strict=False)
        except PydanticValidationError as err:
            handle_pydantic_validation_err(err)

        user = _handle_insert_user(validationResult.model_dump())
        return _generate_res_for_created_user(user)
