from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.http import JsonResponse
from django.middleware.csrf import get_token


# LOGIN
Login = TokenObtainPairView

# GET REFRESH TOKENS
TokenRefresh = TokenRefreshView


# GET CSRF TOKEN
def get_csrf_token(request):
    return JsonResponse({"csrf_token": get_token(request)})
