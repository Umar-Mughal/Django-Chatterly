import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTUtil:
    @staticmethod
    def verify_token(token):
        try:
            simplejwt_token = JWTAuthentication().get_validated_token(token)
            if simplejwt_token and isinstance(simplejwt_token, AccessToken):
                decoded_token = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                return decoded_token
            else:
                return None
        except Exception as e:
            return None
