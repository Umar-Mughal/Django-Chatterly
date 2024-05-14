# PACKAGES
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status
from django.urls import reverse

# MODELS
from apps.authentication.models import User

# SERIALIZER
from apps.authentication.serializers.user_serializer import UserSerializer

# UTILS
from apps.authentication.utils import Util


@api_view(["POST"])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        User.objects.create_user(**serializer.validated_data)
        # Send registration email
        # send_registration_email(request, serializer.validated_data)
        # Send response
        return Response(
            "Your registration has been successful. Please verify your email.",
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_registration_email(request, data):
    user = User.objects.get(email=data["email"])
    access_token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request)
    domain = current_site.domain
    relative_link = reverse("verify-email")
    url = "http://" + domain + relative_link + "?token=" + str(access_token)
    # EMAIL DATA
    to = [user.email]
    subject = "Verify your email"
    body = (
        "Hi " + user.first_name + " use this link below to verify your email \n" + url
    )
    data = {"to": to, "subject": subject, "body": body}
    Util.send_email(data)


@api_view(["GET"])
def verify_email(request):
    pass


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
