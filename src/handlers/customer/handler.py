import http
import json

from ..commons.abstract_functions import abstract_handler
from src.base.entity.customer import Customer
from ..commons.response import Response
from src.base.db import AlchemyEncoder, get_session
import jsonschema
from jsonschema import validate

__default_headers__ = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true"
}


schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Customer",
    "description": "A Customer request json",
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "fullname": {
            "type": "string"
        },
        "nickname": {
            "type": "string"
        },
        "id": {
            "type": "number"
        }
    },
    "required": [
        "id",
        "name",
        "fullname",
        "nickname"
    ]
}


def get(event, context):
    def __get(event, context, session):
        customers = Customer.get_all(session)
        return Response(status_code=200, body=json.dumps(customers, cls=AlchemyEncoder))

    return abstract_handler(event, context, __get)


def create(event, context):
    try:
        validate(instance=event.input.body, schema=schema)
        session = get_session()
        Customer(event.input.body).create(session)
    except jsonschema.exceptions.ValidationError as e:
        return Response(status_code=http.HTTPStatus.BAD_REQUEST, body="Wrong json structure.")


def update(event, context):
    try:
        validate(instance=event.input.body, schema=schema)
        session = get_session()
        Customer(event.input.body).update(session)
    except jsonschema.exceptions.ValidationError as e:
        return Response(status_code=http.HTTPStatus.BAD_REQUEST, body="Wrong json structure.")
