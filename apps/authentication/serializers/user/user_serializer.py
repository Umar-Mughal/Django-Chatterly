# Packages
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

# Models
from apps.authentication.models import User
from apps.authentication.models import EmailVerification

# Utils
from apps.authentication.utils import UserUtil, SendAuthEmailUtil


class RegisterUserSerializer(serializers.ModelSerializer):

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
        validated_data["username"] = UserUtil.generate_unique_username(
            validated_data["email"]
        )

        user = User.objects.create_user(validated_data)
        request = self.context.get("request")
        SendAuthEmailUtil.send_verification_email(
            user.id, SendAuthEmailUtil.EMAIL_TYPES["register"]
        )
        return user

    def update(self, instance, validated_data):
        # raise serializers.ValidationError("Password is not allowed to update")
        password = validated_data.pop(
            "password", None
        )  # Remove password from validated data if not provided
        if password is not None:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
        ]

    def update(self, instance, validated_data):
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
        err = UserUtil.validate_password(self, data)
        if err["status"]:
            raise serializers.ValidationError(err["msg"])
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        err = UserUtil.validate_password(self, data)
        if err["status"]:
            raise serializers.ValidationError(err["msg"])
        return data
