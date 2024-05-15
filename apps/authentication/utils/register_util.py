# Packages
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

# Models
from apps.authentication.models import User, EmailVerification

# Utils
from utils import EmailUtil


class RegisterUtil:
    @staticmethod
    def generate_unique_username(email):
        # Use email prefix as username
        username = email.split("@")[0]
        # Ensure username is unique
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{username}_{suffix}"
            suffix += 1
        return username

    @staticmethod
    def send_email_verify_email(request, email):
        user = User.objects.get(email=email)
        # Six digit code as well for extra security
        email_verification_code = RegisterUtil.update_or_create_code(user)

        access_token = RegisterUtil.generate_jwt_access_token(
            user, email_verification_code
        )
        current_site = get_current_site(request)
        domain = current_site.domain
        relative_link = reverse("verify-email")
        url = "http://" + domain + relative_link + "?token=" + str(access_token)
        # EMAIL DATA
        to = [user.email]
        subject = "Verify your email"
        body = (
            "Hi "
            + user.first_name
            + " use this link below to verify your email \n"
            + url
        )
        data = {"to": to, "subject": subject, "body": body}
        # Send email
        EmailUtil.send_email(data)

    @classmethod
    def generate_six_digit_unique_code(cls):
        return "".join([str(random.randint(0, 9)) for _ in range(6)])

    @classmethod
    def update_or_create_code(cls, user):
        code = RegisterUtil.generate_six_digit_unique_code()
        data = {"code": code, "sent_at": timezone.now()}
        unique_criteria = {"user": user}
        obj, created = EmailVerification.objects.get_or_create(
            **unique_criteria, defaults=data
        )

        if not created:
            obj.code = data["code"]
            obj.sent_at = data["sent_at"]
            obj.save()

        return code

    @classmethod
    def generate_jwt_access_token(cls, user, code):
        custom_payload = {
            "user_id": user.id,
            "data": {
                "code": code,
            },
            "exp": timezone.now() + timedelta(minutes=2),
        }
        token = RefreshToken.for_user(user)
        token.payload.update(custom_payload)
        return token.access_token
