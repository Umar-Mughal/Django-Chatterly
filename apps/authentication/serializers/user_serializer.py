# Packages
from django.utils import timezone
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.conf import settings

# Models
from apps.authentication.models import User
from apps.authentication.models import EmailVerification

# Utils
from apps.authentication.utils import Util


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "last_name",
            "email",
            "password",
            "is_email_verified",
        ]
        read_only_fields = [
            "id",
            "is_email_verified",
        ]  # Make id field read-only (for update)
        write_only_fields = ["password"]

    def create(self, validated_data):
        email = validated_data["email"].lower()
        validated_data["email"] = email
        validated_data["username"] = RegisterUtil.generate_unique_username(
            validated_data["email"]
        )

        user = User.objects.create_user(validated_data)
        # Send email verification email
        request = self.context.get("request")
        RegisterUtil.send_email_verify_email(request, email)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop(
            "password", None
        )  # Remove password from validated data if not provided
        if password is not None:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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
        Util.send_email(data)

    @staticmethod
    def generate_six_digit_unique_code():
        return "".join([str(random.randint(0, 9)) for _ in range(6)])

    @staticmethod
    def update_or_create_code(user):
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

    @staticmethod
    def generate_jwt_access_token(user, code):
        custom_payload = {
            "user_id": user.id,
            "data": {
                "code": code,
            },
            "exp": timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
        }
        token = RefreshToken.for_user(user)
        token.payload.update(custom_payload)
        return token.access_token
