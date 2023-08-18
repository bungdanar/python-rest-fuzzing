from flask_restful import abort
from marshmallow import ValidationError


def handle_ma_validation_err(err: ValidationError):
    statusCode = 400
    abort(statusCode, message=str(err), statusCode=statusCode)
