from flask_restful import abort
from marshmallow import ValidationError as MaValidationError
from pydantic import ValidationError as PydanticValidationError


def handle_ma_validation_err(err: MaValidationError):
    statusCode = 400
    abort(statusCode, message=str(err), statusCode=statusCode)


def handle_pydantic_validation_err(err: PydanticValidationError):
    statusCode = 400
    abort(statusCode, message=str(err), statusCode=statusCode)
