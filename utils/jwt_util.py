import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken as SimpleJWTInvalidToken

# Utils
from utils.exceptions import InvalidToken


class JWTUtil:
    @staticmethod
    def verify_token(token):
        try:
            if not token:
                raise InvalidToken("Token is not provided")
            validated_token = JWTAuthentication().get_validated_token(token)
            if not validated_token or not isinstance(validated_token, AccessToken):
                raise InvalidToken("Token is invalid or expired")
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except SimpleJWTInvalidToken as e:
            raise InvalidToken("Token is invalid")
