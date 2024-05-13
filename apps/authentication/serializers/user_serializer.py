# serializers.py
from rest_framework import serializers
from apps.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
        ]
        read_only_fields = ["id"]  # Make id field read-only (for update)
        write_only_fields = ["password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = User.objects.create_user(
            email=email, password=password, **validated_data
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
