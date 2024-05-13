from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework import status
from apps.user.models.user_model import User

from apps.user.serializers.user_serializer import UserSerializer

"""
Making use of GenericViewSet, because only needed user creation (registration) and updation, and also custom  methods. No need for users list, and retrieve single user by id. So that's the perfect use case of using  GenericViewSet, of course URLs for custom methods will be automatically generated as well, based on thier names. So that's the benefit we get with viewsets.

Also I needed to user create_user method for creation, that was also the reason to to customize create method. 

"""


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return []
        else:
            return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.data)
            user_serializer = self.get_serializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def account(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
