import unittest

import src.handlers.auth.handler as handler
from src.handlers.exception import UnauthorizedException
import logging
logging.disable(logging.CRITICAL)


class AuthorisationHandler(unittest.TestCase):
    def test__JWT_validation__not_set_JWT(self):
        # GIVEN event is empty JSON
        event = {}

        # WHEN call auth to authorizer caller
        # THEN throws UnauthorizedException
        with self.assertRaises(UnauthorizedException):
            handler.auth(event, None)

    def test__JWT_validation__value_is_not_a_JWT(self):
        # GIVEN event has authorizationToken with not JWT structure
        event = {
            "authorizationToken": "Test"
        }

        # WHEN call auth to authorizer caller
        # THEN throws UnauthorizedException
        with self.assertRaises(UnauthorizedException):
            handler.auth(event, None)

    def test__JWT_validation__JWT_without_bearer(self):
        # GIVEN event has authorizationToken, but hasn't prefix Bearer
        event = {
            "authorizationToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
                                  ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c "
        }

        # WHEN call auth to authorizer caller
        # THEN throws UnauthorizedException
        with self.assertRaises(UnauthorizedException):
            handler.auth(event, None)

    def test__JWT_validation__JWT_without_token(self):
        # GIVEN event has authorizationToken, but hasn't correct token
        event = {
            "authorizationToken": "Bearer"
        }

        # WHEN call auth to authorizer caller
        # THEN throws UnauthorizedException
        with self.assertRaises(UnauthorizedException):
            handler.auth(event, None)

    def test__JWT_validation__JWT_without_secret_key(self):
        # GIVEN event has authorizationToken, but hasn't correct token
        event = {
            "authorizationToken": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ "
        }
        handler.JWT_ALGORITHM = "HS256"
        handler.SECRET_KEY = "your-256-bit-secret"

        # WHEN call auth to authorizer caller
        # THEN throws UnauthorizedException
        with self.assertRaises(UnauthorizedException):
            handler.auth(event, None)

    def test__JWT_validation__JWT_with_not_correct_header(self):
        # GIVEN event has authorizationToken, but hasn't correct token
        event = {
            "authorizationToken": "Bearer JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
                                  ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c "
        }
        handler.JWT_ALGORITHM = "HS256"
        handler.SECRET_KEY = "your-256-bit-secret"

        # WHEN call auth to authorizer caller
        # THEN throws UnauthorizedException
        with self.assertRaises(UnauthorizedException):
            handler.auth(event, None)

    def test__JWT_validation__JWT_with_correct_event(self):
        # GIVEN event has authorizationToken, but hasn't correct token
        event = {
            "authorizationToken": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
                                  ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            "methodArn": "arn:aws:execute-api:us-east-1:123456789012:abcdef123/test/GET/request"
        }
        handler.JWT_ALGORITHM = "HS256"
        handler.SECRET_KEY = "your-256-bit-secret"

        # WHEN call auth to authorizer caller
        result = handler.auth(event, None)

        # THEN API GATEWAY take correct access
        EXPECTED = {
            'principalId': 'anonymous',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": 'Allow',
                        "Resource": 'arn:aws:execute-api:us-east-1:123456789012:abcdef123/test/GET/request'

                    }
                ]
            }
        }
        self.assertEqual(EXPECTED, result)


if __name__ == '__main__':
    unittest.main()
