# PACKAGES
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# VIEWS
from apps.authsys.views.api import user_view
from apps.authsys.views.api import auth_view

router = DefaultRouter()
router.register("", user_view.UserViewSet)
urlpatterns = [
    path("/", include(router.urls)),
    # path(
    #     "/account",
    #     UserViewSet.get_account({"get": "get_account"}),
    # ),
    # Authentication
    # On login get Tokens
    path("/tokens/pair/", auth_view.Login.as_view(), name="token_obtain_pair"),
    path(
        "/tokens/pair/refresh", auth_view.TokenRefresh.as_view(), name="token_refresh"
    ),
    path("/tokens/csrf/", auth_view.get_csrf_token),
]
