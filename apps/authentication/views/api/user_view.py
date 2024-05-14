# PACKAGES
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status

# MODELS
from apps.authentication.models import User
from apps.authentication.models import EmailVerification

# SERIALIZER
from apps.authentication.serializers.user_serializer import UserSerializer

# UTILS
from utils.jwt_util import verify_token


@api_view(["POST"])
def user_create(request):
    serializer = UserSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            "Your registration has been successful. Please verify your email.",
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def verify_email(request):
    try:
        token = request.query_params.get("token")
        if not token:
            raise ValueError("Token is not provided")
        decoded_token = verify_token(token)
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
