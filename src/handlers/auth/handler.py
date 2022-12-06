from src.handlers.exception import UnauthorizedException
import os
import logging
import jwt
from jwt import exceptions

logging.basicConfig(encoding='utf-8', level=os.getenv('LOG_LEVEL', logging.INFO))
log = logging.getLogger()

# Set by serverless.yml
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOW_ACCESS_TO_SERVICE = "Allow"
PRINCIPAL_ID = 'anonymous'


def auth(event, context):
    request_auth_token = event.get('authorizationToken')
    method_arn = event.get("methodArn")

    if not request_auth_token:
        raise UnauthorizedException()

    try:
        token_method, auth_token = request_auth_token.split(' ')

    except Exception:
        log.exception("Failing due to invalid authorizationToken field structure.")
        raise UnauthorizedException()

    if not (token_method.lower() == 'bearer' and auth_token):
        log.exception("Failing due to invalid token_method or missing auth_token.")
        raise UnauthorizedException()

    try:
        jwt_verify(auth_token, SECRET_KEY)
        policy = generate_policy(PRINCIPAL_ID, method_arn)
        return policy

    except exceptions.InvalidSignatureError as e:
        log.exception(f'Validation secret key failed: {e}.')
        raise UnauthorizedException()

    except Exception as e:
        log.exception(f'Exception encountered: {e}.')
        raise UnauthorizedException()


def jwt_verify(auth_token, secret):
    payload = jwt.decode(auth_token, secret, algorithms=[JWT_ALGORITHM])
    return payload['sub']


def generate_policy(principal_id, resource, effect=ALLOW_ACCESS_TO_SERVICE):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource

                }
            ]
        }
    }
