from rest_framework import viewsets, generics, views
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.post.models import Post
from apps.post.serializers.post_serializer import PostSerializer
import time


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UploadPost(views.APIView):
    def post(self, request):
        time.sleep(2)
        return Response("hello World")
