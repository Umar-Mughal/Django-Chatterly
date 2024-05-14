# PACKAGES
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from django.shortcuts import get_object_or_404


# MODELS
from apps.authentication.models import User
from apps.authentication.models import EmailVerification

# SERIALIZER
from apps.authentication.serializers.user.user_serializer import (
    UserSerializer,
    ResendVerifyEmailSerializer,
)

# UTILS
from utils import JWTUtil
from apps.authentication.utils import RegisterUtil


@api_view(["POST"])
def user_create(request):
    # Validation
    serializer = UserSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)  # throw exception and don't proceed
    # Saving data
    serializer.save()
    # Sending response
    return Response(
        "Your registration has been successful. Please verify your email.",
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def verify_email(request):
    try:
        token = request.query_params.get("token")
        if not token:
            raise ValueError("Token is not provided")
        decoded_token = JWTUtil.verify_token(token)
        if decoded_token is None:
            raise ValueError("Token is invalid or expired")

        user_id = decoded_token["user_id"]
        user = User.objects.get(pk=user_id)
        if user.is_email_verified:
            return Response(
                "Email already verified",
            )
        code = decoded_token["data"]["code"]
        email_verification_instance = EmailVerification.objects.get(
            user=user_id, code=code
        )
        user.is_email_verified = True
        user.save()
        return Response("Email verified successfully")
    except User.DoesNotExist as e:
        return Response(
            "Token is invalid or expired", status=status.HTTP_400_BAD_REQUEST
        )
    except ValueError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response("Something went wrong!!!", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def resend_verify_email(request):
    # VALIDATION
    serializer = ResendVerifyEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    user = get_object_or_404(User, email="umar@gmail.com")
    if user.is_email_verified:
        return Response("Email is already verified", status=status.HTTP_403_FORBIDDEN)
    # RegisterUtil.send_email_verify_email(request, email)
    return Response("Verification email sent. Please check your email")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_get(request):
    try:
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def user_delete(request):
    return Response("Pending")


@api_view(["UPDATE"])
@permission_classes([IsAuthenticated])
def user_update(request):
    return Response("Update is pending")
