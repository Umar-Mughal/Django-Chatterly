# PACKAGES
from django.urls import path

# VIEWS
from apps.authentication.views.api import user_view
from apps.authentication.views.api import authn_view


urlpatterns = [
    # --- USER MANAGEMENT: ON ----#
    # 1. REGISTRATION
    path("/register/", user_view.user_create, name="create-account"),
    path("/verify-email/", user_view.verify_email, name="verify-email"),
    path(
        "/resend-verify-email/",
        user_view.resend_verify_email,
        name="resend-verify-email",
    ),
    # 2. RESET PASSWORD
    path("/password-reset/", user_view.user_get, name="password-reset"),
    path("/password-reset-confirm/", user_view.user_get, name="password-reset-confirm"),
    # 3. GET ACCOUNT
    path("/my-account/", user_view.user_get, name="get-account"),
    # 4. UPDATE ACCOUNT
    path("/update/", user_view.user_update, name="update-account"),
    # 5. DELETE ACCOUNT
    path("/delete/", user_view.user_delete, name="delete-account"),
    # --- USER MANAGEMENT: OFF ----#
    # --- AUTHENTICATION MANAGEMENT: ON ----#
    path("/login/", authn_view.Login.as_view(), name="token_obtain_pair"),
    path("/token/refresh", authn_view.TokenRefresh.as_view(), name="token_refresh"),
    path("/token/csrf/", authn_view.get_csrf_token),
    # --- AUTHENTICATION MANAGEMENT: OFF ----#
]
