# PACKAGES
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# VIEWS
from apps.authsys.views.api import user_view
from apps.authsys.views.api import authn_view

router = DefaultRouter()
# router.register("", user_view.UserViewSet)
urlpatterns = [
    # path("/account/", include(router.urls)),
    # path(
    #     "/account",
    #     UserViewSet.get_account({"get": "get_account"}),
    # ),
    # ACCOUNT
    path("/account/", user_view.user_create, name="create-account"),
    path("/account/get/", user_view.user_delete, name="get-account"),
    path("/account/update/", user_view.user_update, name="update-account"),
    path("/account/delete/", user_view.user_create, name="delete-account"),
    # Authentication
    path("/authn/login/", authn_view.Login.as_view(), name="token_obtain_pair"),
    path("/authn/refresh", authn_view.TokenRefresh.as_view(), name="token_refresh"),
    path("/authn/csrf/", authn_view.get_csrf_token),
]
