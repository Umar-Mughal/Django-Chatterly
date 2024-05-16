# Packages
from rest_framework import serializers
import re


# Models
from apps.authentication.models import User
from apps.authentication.models import EmailVerification

# Utils
from apps.authentication.utils import RegisterUtil, SendAuthEmailUtil


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
        request = self.context.get("request")
        SendAuthEmailUtil.send_verification_email(
            request, user, SendAuthEmailUtil.EMAIL_TYPES["register"]
        )
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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        # Check if passwords match
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        # Check if password meets strength requirements
        # if not self.is_strong_password(password):
        #     raise serializers.ValidationError(
        #         "Password must be 8 characters long and contain at least one upper case letter, one lowercase letter, one digit, and one special character."
        #     )
        return data

    def is_strong_password(self, password):
        # Define regex pattern for strong password requirements
        pattern = (
            r"^(?=.*[A-Z])"  # At least one uppercase letter
            r"(?=.*[a-z])"  # At least one lowercase letter
            r"(?=.*\d)"  # At least one digit
            r"(?=.*[@$!%*#?&])"  # At least one special character
            r".{8,}$"  # At least 8 characters long
        )

        # Check if password matches the regex pattern
        return bool(re.match(pattern, password))
