# PACKAGES
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    permission_classes,
    api_view,
    authentication_classes,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, reverse

# MODELS
from apps.authentication.models import User
from apps.authentication.models import EmailVerification

# SERIALIZER
from apps.authentication.serializers.user.user_serializer import (
    UserSerializer,
    EmailSerializer,
)

# UTILS
from utils import JWTUtil, NoAuthentication
from apps.authentication.utils import SendAuthEmailUtil
from utils.exceptions import InvalidToken


@api_view(["POST"])
def user_create(request):
    # Validation
    serializer = UserSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)  # throw exception and don't proceed

    # Save data, serializer crate() will be called on
    serializer.save()

    # Send response
    return Response(
        "Your registration has been successful. Please verify your email.",
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@authentication_classes([NoAuthentication])
@permission_classes([AllowAny])
def verify_email(request):
    try:
        # 1. Verify token
        decoded_token = JWTUtil.verify_token(request.query_params.get("token"))

        # 2. Check if email is already verified
        user_id = decoded_token["user_id"]
        user = User.objects.get(pk=user_id)
        if not user:
            raise InvalidToken("Token is invalid or expired")

        if user.is_email_verified:
            raise ValueError("Email is already verified")

        # 3. Check six-digit code, that we put for extra security & delete it
        code = decoded_token["data"]["code"]
        email_type = decoded_token["data"]["email_type"]
        email_verification_instance = EmailVerification.objects.get(
            user=user_id, code=code, email_type=email_type
        )
        if not email_verification_instance:
            raise InvalidToken("Token code is invalid or expired")

        email_verification_instance.delete()

        # 4. Mark email as verified
        user.is_email_verified = True
        user.save()

        # 5. Send response
        return Response("Email verified successfully")
    except (InvalidToken, ValueError) as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def resend_email_verification_email(request):
    # 1. Validation
    srl = EmailSerializer(data=request.data)
    srl.is_valid(raise_exception=True)

    # 2. Get user or send 404
    email = email = srl.validated_data["email"]
    user = get_object_or_404(User, email=email)

    # 3. Check if email is already verified
    if user.is_email_verified:
        return Response("Email is already verified", status=status.HTTP_403_FORBIDDEN)

    # 4. Send email
    SendAuthEmailUtil.send_verification_email(
        request,
        user,
        SendAuthEmailUtil.EMAIL_TYPES["register"],
    )
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


# @api_view(["POST"])
# def send_password_reset_email(request):
#     return Response(
#         "Sending password reset email is pending. This will be trigerred when forntend will send an email in forgot password"
#     )


@api_view(["POST"])
def send_password_reset_email(request):
    # 1. Validation
    srl = EmailSerializer(data=request.data)
    srl.is_valid(raise_exception=True)

    # 2. Get user or send 404
    email = email = srl.validated_data["email"]
    user = get_object_or_404(User, email=email)

    # 3. Send email
    SendAuthEmailUtil.send_verification_email(
        request,
        user,
        SendAuthEmailUtil.EMAIL_TYPES["reset_password"],
    )
    return Response("Password reset link sent. Please check your email.")


# @api_view(["POST"])
# def reset_password(request):
#     # A user will submit request with the token which was sent in send_password_reset_email
#     return Response("Reset your password Pending") @ api_view(["POST"])


@api_view(["POST"])
def reset_password(request):
    try:
        # 1. Verify token
        decoded_token = JWTUtil.verify_token(request.query_params.get("token"))

        # 2. Check if email is already verified
        user_id = decoded_token["user_id"]
        user = User.objects.get(pk=user_id)
        if not user:
            raise InvalidToken("Token is invalid or expired")

        if user.is_email_verified:
            raise ValueError("Email is already verified")

        # 3. Check six-digit code, that we put for extra security & delete it
        code = decoded_token["data"]["code"]
        email_type = decoded_token["data"]["email_type"]
        email_verification_instance = EmailVerification.objects.get(
            user=user_id, code=code, email_type=email_type
        )
        if not email_verification_instance:
            raise InvalidToken("Token code is invalid or expired")

        email_verification_instance.delete()

        # 4. Mark email as verified
        user.is_email_verified = True
        user.save()

        # 5. Send response
        return Response("Email verified successfully")
    except (InvalidToken, ValueError) as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def user_delete(request):
    return Response("Pending")


@api_view(["UPDATE"])
@permission_classes([IsAuthenticated])
def user_update(request):
    return Response("Update is pending")
