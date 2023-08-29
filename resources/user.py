from flask import jsonify, request
from flask_restful import Resource

from models.user import UserModel
from models.role import RoleModel
from common.db import db
from common.response_schema import user_res_schema


def _handle_insert_user(data):
    role = RoleModel.query.get(2)

    user = UserModel(**data)
    user.roles.append(role)

    db.session.add(user)
    db.session.commit()

    return user


def _generate_res_for_created_user(user: UserModel):
    response = jsonify(user_res_schema.dump(user))
    response.status_code = 201
    return response


class UserResource(Resource):
    def post(self):
        data = request.get_json()

        user = _handle_insert_user(data)
        return _generate_res_for_created_user(user)
