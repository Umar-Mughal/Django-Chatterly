import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication


def verify_token(token):
    try:
        jwt_token = JWTAuthentication().get_validated_token(token)
        if jwt_token and isinstance(jwt_token, AccessToken):
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        else:
            return None
    except Exception as e:
        return None
