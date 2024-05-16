# Packages
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken as SimpleJWTInvalidToken

# Models
from apps.authentication.models import EmailVerification

# Utils
from utils import EmailUtil
from utils.exceptions import InvalidToken


# class EmailContent:
#     @staticmethod
#     def register_email_content(user, url):
#         subject = "Welcome to our platform!"
#         body = f"Hi {user.first_name}, welcome to our platform! Please verify your email address by clicking the link below:\n{url}"
#         return subject, body
#
#     @staticmethod
#     def reset_password_email_content(user, url):
#         subject = "Password reset request"
#         body = f"Hi {user.first_name}, you request a password reset, Click the link below to reset your password:\n {url}"
#         return subject, body


class SendAuthEmailUtil:
    EMAIL_TYPES = EmailVerification.EMAIL_TYPES
    MODEL = EmailVerification

    @staticmethod
    def send_verification_email(request, user, email_type):
        # 1. Get six-digit code
        code = SendAuthEmailUtil.generate_verification_code(user, email_type)

        # 2. Generate jwt token with custom payload (including code)
        jwt_data = {"user": user, "code": code, "email_type": email_type}
        access_token = SendAuthEmailUtil.generate_jwt_access_token(jwt_data)

        # 3. Build page URL
        route = SendAuthEmailUtil.get_route(email_type)
        url = request.build_absolute_uri(route + "?token=" + str(access_token))

        # 4. Get email content (subject, body, attachment etc)
        # subject, body = email_content(user, url)
        subject, body = SendAuthEmailUtil.get_email_content(email_type, user, url)

        # Send email
        EmailUtil.send_email({"to": [user.email], "subject": subject, "body": body})

    @classmethod
    def generate_verification_code(cls, user, email_type):
        six_digit_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        data = {
            "code": six_digit_code,
            "sent_at": timezone.now(),
            "email_type": email_type,
        }
        unique_criteria = {"user": user}
        obj, created = cls.MODEL.objects.get_or_create(**unique_criteria, defaults=data)

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
        email_type = data["email_type"]

        custom_payload = {
            "user_id": user.id,
            "data": {"code": code, "email_type": email_type},
            "exp": timezone.now() + timedelta(minutes=2),
        }
        token = RefreshToken.for_user(user)
        token.payload.update(custom_payload)
        return token.access_token

    @classmethod
    def get_email_content(cls, email_type, user, url):
        if email_type == cls.EMAIL_TYPES["register"]:
            subject = "Welcome to our platform!"
            body = f"Hi {user.first_name}, welcome to our platform! Please verify your email address by clicking the link below:\n{url}"
            return subject, body
        elif email_type == cls.EMAIL_TYPES["reset_password"]:
            subject = "Password reset request"
            body = f"Hi {user.first_name}, you request a password reset, Click the link below to reset your password:\n {url}"
            return subject, body

    @classmethod
    def get_route(cls, email_type):
        if email_type == cls.EMAIL_TYPES["register"]:
            return reverse("verify-email")
        if email_type == cls.EMAIL_TYPES["reset_password"]:
            return reverse("reset-password")


class VerifyAuthEmailUtil:
    @staticmethod
    def verify_jwt_token(token):
        try:
            if not token:
                raise InvalidToken("Token is not provided")
            validated_token = JWTAuthentication().get_validated_token(token)
            if not validated_token or not isinstance(validated_token, AccessToken):
                raise InvalidToken("Token is invalid or expired")
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except SimpleJWTInvalidToken as e:
            raise InvalidToken("Token is invalid")


class EmailContentUtil:
    @staticmethod
    def register_email_content(user, url):
        subject = "Welcome to our platform!"
        body = f"Hi {user.first_name}, welcome to our platform! Please verify your email address by clicking the link below:\n{url}"
        return subject, body

    @staticmethod
    def reset_password_email_content(user, url):
        subject = "Password reset request"
        body = f"Hi {user.first_name}, you request a password reset, Click the link below to reset your password:\n {url}"
        return subject, body

    #         subject = "Password Reset Request"
    #         body = f"Hi {user.first_name}, you requested a password reset. Click the link below to reset your password: {url}"
