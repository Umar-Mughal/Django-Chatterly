from rest_framework import serializers
from apps.post.models.post_model import Post
from apps.post.models.tag_model import Tag
from apps.authsys.models.user_model import User


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    file = serializers.FileField(required=False)
    post_url = serializers.URLField(required=False)
    location = serializers.CharField(max_length=255, required=False)
    featured_image = serializers.ImageField(required=False)
    comments_enabled = serializers.BooleanField(default=True)
    post_type = serializers.ChoiceField(
        choices=Post.POST_TYPE_CHOICES, default="status"
    )
    privacy_settings = serializers.ChoiceField(
        choices=Post.PRIVACY_CHOICES, default="public"
    )
    status = serializers.ChoiceField(choices=Post.POST_STATUS_CHOICES, default="draft")
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.file = validated_data.get("file", instance.file)
        instance.post_url = validated_data.get("post_url", instance.post_url)
        instance.location = validated_data.get("location", instance.location)
        instance.featured_image = validated_data.get(
            "featured_image", instance.featured_image
        )
        instance.comments_enabled = validated_data.get(
            "comments_enabled", instance.comments_enabled
        )
        instance.post_type = validated_data.get("post_type", instance.post_type)
        instance.privacy_settings = validated_data.get(
            "privacy_settings", instance.privacy_settings
        )
        instance.status = validated_data.get("status", instance.status)
        instance.user = validated_data.get("user", instance.user)
        instance.tags.set(validated_data.get("tags", instance.tags.all()))
        instance.save()
        return instance
