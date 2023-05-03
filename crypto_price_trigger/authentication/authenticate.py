from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from crypto_price_trigger.authentication.jwt import decode_jwt_token
from crypto_price_trigger.utils.custom_exception import InvalidTokenException


class UserAuthorization(BaseAuthentication):
    """
    Custom user authentication class. Authenticates user using access_token,
    which is retrieved using login via otp.
    """

    def authenticate(self, request):
        if "Authorization" not in request.headers:
            raise AuthenticationFailed(
                {"message": "Please provide token"},
            )
        try:
            access_token = request.headers["Authorization"]
            payload = decode_jwt_token(access_token)
        except InvalidTokenException as e:
            raise AuthenticationFailed(
                {"message": str(e)},
            )
        return payload, None

    def authenticate_header(self, request):
        return "Token"
