from django.urls import path
from apps.authn.views.api import authn_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # On login get Tokens
    path("/tokens/pair/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("/tokens/pair/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/tokens/csrf/", authn_view.get_csrf_token),
]
