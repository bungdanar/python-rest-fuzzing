from flask_restful import abort
from marshmallow import ValidationError


def handle_ma_validation_err(err: ValidationError):
    statusCode = 400

    first_key = next(iter(err.messages))
    first_value = err.messages[first_key][0]

    errMsg = f"{first_key}: {first_value}"

    abort(statusCode, message=errMsg, statusCode=statusCode)
