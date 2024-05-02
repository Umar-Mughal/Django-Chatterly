from django.urls import path
from ...views.api import token_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Tokens
    path("tokens/pair/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokens/pair/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("tokens/csrf/", token_view.get_csrf_token),
]
