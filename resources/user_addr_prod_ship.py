from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError as MaValidationError

from models.user import UserModel
from models.role import RoleModel
from models.address import AddressModel
from models.product import ProductModel
from models.shipping import ShippingModel
from common.db import db
from common.response_schema import user_addr_prod_ship_res_schema
from common.handle_validation_err import handle_ma_validation_err
from common.ma_request_schema import UserAddrProdShipCreatePartialMaValidation, UserAddrProdShipCreateFullMaValidation


def _handle_insert_user(data):
    addresses = itemgetter('addresses')(data)
    addresses = [AddressModel(**a) for a in addresses]

    shipping = itemgetter('shipping')(data)
    shipping = ShippingModel(**shipping)

    product = itemgetter('product')(data)
    product = ProductModel(**product)
    product.shippings.append(shipping)

    role = RoleModel.query.get(2)

    data.pop('addresses')
    data.pop('product')
    data.pop('shipping')

    user = UserModel(**data)
    user.roles.append(role)
    user.addresses.extend(addresses)
    user.products.append(product)

    db.session.add(user)
    db.session.commit()

    return user


def _generate_res_for_created_user(user: UserModel):
    response = jsonify(user_addr_prod_ship_res_schema.dump(user))
    response.status_code = 201
    return response


class UserAddrProdShipResource(Resource):
    def post(self):
        data = request.get_json()

        user = _handle_insert_user(data)
        return _generate_res_for_created_user(user)


class UserAddrProdShipPartialMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrProdShipCreatePartialMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        user = _handle_insert_user(validationResult)
        return _generate_res_for_created_user(user)


class UserAddrProdShipFullMaValidationResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            validationResult = UserAddrProdShipCreateFullMaValidation().load(data)
        except MaValidationError as err:
            handle_ma_validation_err(err)

        user = _handle_insert_user(validationResult)
        return _generate_res_for_created_user(user)
