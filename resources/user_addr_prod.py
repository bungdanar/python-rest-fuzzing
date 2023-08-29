from operator import itemgetter

from flask import jsonify, request
from flask_restful import Resource

from models.user import UserModel
from models.role import RoleModel
from models.address import AddressModel
from models.product import ProductModel
from common.db import db
from common.response_schema import user_addr_prod_res_schema


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
