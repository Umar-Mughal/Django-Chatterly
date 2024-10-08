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
from celery import shared_task
import time
from django.conf import settings
from apps.authentication.models import User

# Models
from apps.authentication.models import EmailVerification

# Utils
from utils import EmailUtil
from utils.exceptions import InvalidToken


class SendAuthEmailUtil:
    EMAIL_TYPES = EmailVerification.EMAIL_TYPES
    MODEL = EmailVerification

    @staticmethod
    def send_verification_email(user_id, email_type):
        result = SendAuthEmailUtil.send_email.delay(user_id, email_type)

    @staticmethod
    @shared_task
    def send_email(userid, email_type):
        # 1. Get User
        user = User.objects.get(id=userid)

        # 2. Get six-digit code
        code = SendAuthEmailUtil.generate_verification_code(user, email_type)

        # 3. Generate jwt token with custom payload (including code)
        jwt_data = {"user": user, "code": code, "email_type": email_type}
        access_token = SendAuthEmailUtil.generate_jwt_access_token(jwt_data)

        # 4. Build page URL
        relative_link = SendAuthEmailUtil.get_route(email_type)
        url = f"{settings.SITE_URL}{relative_link}?token={str(access_token)}"

        # 5. Get email content (subject, body, attachment etc)
        subject, body = SendAuthEmailUtil.get_email_content(email_type, user, url)

        # 6. Send email
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

    """
    Verify six-digit code, that we put for extra security & delete it to clean up database, if not found raise an exception that token is invalid
    """

    @staticmethod
    def verify_code(decoded_token):
        try:
            user_id = decoded_token["user_id"]
            code = decoded_token["data"]["code"]
            email_type = decoded_token["data"]["email_type"]

            email_verification_instance = EmailVerification.objects.get(
                user=user_id, code=code, email_type=email_type
            )

            email_verification_instance.delete()
        except EmailVerification.DoesNotExist as e:
            raise InvalidToken("Token code is invalid or expired")
