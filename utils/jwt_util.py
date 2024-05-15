import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseBadRequest
from rest_framework import status
from rest_framework.exceptions import APIException

from django.http import HttpResponse


class JWTUtil:
    @staticmethod
    def verify_token(token):
        try:
            # Check if token exists
            if not token:
                raise ValueError("Token is not provided")
            simplejwt_token = JWTAuthentication().get_validated_token(token)
            if simplejwt_token and isinstance(simplejwt_token, AccessToken):
                decoded_token = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                return decoded_token
            else:
                raise ValueError("Token is invalid or expired")
        except ValueError as e:
            raise ValueError(e)
        except Exception as e:
            raise ValueError("Token is invalid or expired")
