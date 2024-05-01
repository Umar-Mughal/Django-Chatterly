from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ...serializers.post_serializer import PostCreateSerializer
from ...models.post_model import Post

"""
ON: POST CREATION
"""

"""
V1: Simple Function-Based View (FBV):
"""


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_post_function(request):
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        dummy_user = User.objects.get(username="dummy_user")
        serializer.save(user=dummy_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
V2: Class-Based View (CBV) with APIView
"""


class PostCreateAPIViewClass(APIView):
    def get(self, request):
        return Response({"success": True})

    def post1(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            dummy_user = User.objects.get(username="dummy_user")
            serializer.save(user=dummy_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
V3: Class-Based View (CBV) with CreateAPIView
"""


class PostCreateCreateAPIViewClass(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        # Customize the creation process here
        dummy_user = User.objects.get(username="dummy_user")
        serializer.save(user=dummy_user)


"""
V4: Class-Based View (CBV) with ModelViewSet
"""


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        # Customize the creation process here
        dummy_user = User.objects.get(username="dummy_user")
        serializer.save(user=dummy_user)
        # You can perform additional actions such as sending notifications, etc.

    # Other view set methods like list, retrieve, update, destroy, etc. can be defined here as well


# V5: Using ViewSets with Routers:
# from rest_framework.routers import DefaultRouter
# from .views import PostViewSet
#
# router = DefaultRouter()
# router.register(r"posts", PostViewSet, basename="post")
# urlpatterns = router.urls

"""
OFF: POST CREATION
"""
