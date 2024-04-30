from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ...serializers.post_serializer import PostCreateSerializer


@api_view(["POST"])
def create_post(request):
    print("request data -------", request)
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
