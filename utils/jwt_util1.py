import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import status
from rest_framework.response import Response


# class JWTUtil:
#     @staticmethod
#     def verify_token(token):
#         try:
#             if not token:
#                 return Response(
#                     "Token is not provided", status=status.HTTP_400_BAD_REQUEST
#                 )
#             simplejwt_token = JWTAuthentication().get_validated_token(token)
#             if simplejwt_token and isinstance(simplejwt_token, AccessToken):
#                 decoded_token = jwt.decode(
#                     token, settings.SECRET_KEY, algorithms=["HS256"]
#                 )
#                 return decoded_token
#             else:
#                 return None
#         except Exception as e:
#             return None
class JWTUtil:
    @staticmethod
    def verify_token(token):
        try:
            if not token:
                # raise ValueError("Token is not provided1")
                return Response("token is missing")
            simplejwt_token = JWTAuthentication().get_validated_token(token)
            if simplejwt_token and isinstance(simplejwt_token, AccessToken):
                decoded_token = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                return decoded_token
            else:
                return None
        except Exception as e:
            print("-----55555", e)
            raise (e)
