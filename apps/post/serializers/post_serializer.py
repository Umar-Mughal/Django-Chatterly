from rest_framework import serializers
from ..models.post_model import Post

"""
ON: PostCreateSerializer 
"""


class PostCreateSerializer(serializers.Serializer):
    content = serializers.CharField()
    post_type = serializers.ChoiceField(choices=Post.POST_TYPE_CHOICES)
    privacy_settings = serializers.ChoiceField(choices=Post.PRIVACY_CHOICES)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


"""
OFF
"""
