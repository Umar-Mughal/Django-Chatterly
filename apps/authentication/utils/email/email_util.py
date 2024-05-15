# Packages
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

# Models
from apps.authentication.models import EmailVerification

# Utils
from utils import EmailUtil


class EmailVerificationUtil:
    EMAIL_TYPES = EmailVerification.EMAIL_TYPES
    MODEL = EmailVerification

    @staticmethod
    def send_verification_email(request, user, route, email_content):
        # 1. Get six-digit code
        code = EmailVerificationUtil.generate_verification_code(user)

        # 2. Generate jwt token with custom payload (including code)
        jwt_data = {"user": user, "code": code}
        access_token = EmailVerificationUtil.generate_jwt_access_token(jwt_data)

        # 3. Build page URL
        url = request.build_absolute_uri(route + "?token=" + str(access_token))

        # 4. Get email content (subject, body, attachment etc)
        subject, body = email_content(user, url)

        # Send email
        EmailUtil.send_email({"to": [user.email], "subject": subject, "body": body})

    @classmethod
    def generate_verification_code(cls, user):
        six_digit_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        data = {"code": six_digit_code, "sent_at": timezone.now()}
        unique_criteria = {"user": user}
        obj, created = EmailVerification.objects.get_or_create(
            **unique_criteria, defaults=data
        )

        if not created:
            obj.code = data["code"]
            obj.sent_at = data["sent_at"]
            obj.email_type = data["email_type"]
            obj.save()

        return six_digit_code

    @classmethod
    def generate_jwt_access_token(cls, data):
        user = data["user"]
        code = data["code"]
        custom_payload = {
            "user_id": user.id,
            "data": {"code": code},
            "exp": timezone.now() + timedelta(minutes=2),
        }
        token = RefreshToken.for_user(user)
        token.payload.update(custom_payload)
        return token.access_token

    @classmethod
    def get_email_content(cls, user, email_type, url):
        if email_type == "registration":
            subject = "Welcome to our platform!"
            body = f"Hi {user.first_name}, welcome to our platform! Please verify your email address by clicking the link below:\n {url}"
        elif email_type == "password_reset":
            subject = "Password Reset Request"
            body = f"Hi {user.first_name}, you requested a password reset. Click the link below to reset your password: {url}"
        else:
            # Default fallback
            subject = "Verify your email"
            body = (
                f"Hi {user.first_name}, use this link below to verify your email: {url}"
            )

        return subject, body
