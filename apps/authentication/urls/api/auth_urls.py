# PACKAGES
from django.urls import path

# VIEWS
from apps.authentication.views.api import user_view
from apps.authentication.views.api import authn_view

urlpatterns = [
    # USER MANAGEMENT (CRUD)
    path("/register/", user_view.user_create, name="create-account"),
    path("/verify-email/", user_view.user_create, name="verify-email"),
    path("/my-account/", user_view.user_get, name="get-account"),
    path("/update/", user_view.user_update, name="update-account"),
    path("/delete/", user_view.user_delete, name="delete-account"),
    # AUTHENTICATION MANAGEMENT
    path("login/", authn_view.Login.as_view(), name="token_obtain_pair"),
    path("token/refresh", authn_view.TokenRefresh.as_view(), name="token_refresh"),
    path("token/csrf/", authn_view.get_csrf_token),
]
