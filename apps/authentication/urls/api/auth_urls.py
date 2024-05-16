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
        "/resend-email-verification-email/",
        user_view.resend_email_verification_email,
        name="resend-email-verification-email",
    ),
    # 2. RESET PASSWORD
    path(
        "/forgot-password/",
        user_view.send_password_reset_email,
        name="send-password-reset-email",
    ),
    path(
        "/reset-password/",
        user_view.reset_password,
        name="reset-password",
    ),
    # 3. GET ACCOUNT
    path("/me/", user_view.user_get, name="get-account"),
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
