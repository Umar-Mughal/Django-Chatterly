# Packages
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import views
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status

# Serializers
from apps.authentication.serializers.authn.login_serializer import LoginSerializer


# LOGIN
class Login(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Throw exception if validation fails

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_email_verified:
            return Response(
                "Please verify your email", status=status.HTTP_403_FORBIDDEN
            )

        return get_tokens_for_user(user)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


# GET REFRESH TOKENS
TokenRefresh = TokenRefreshView


# GET CSRF TOKEN
def get_csrf_token(request):
    return JsonResponse({"csrf_token": get_token(request)})
