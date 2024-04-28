from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    PRIVACY_CHOICES = [
        ("public", "Public"),
        ("friends_only", "Friends Only"),
        ("private", "Private"),
    ]

    POST_TYPE_CHOICES = [
        ("status", "Status Update"),
        ("photo", "Photo"),
        ("video", "Video"),
        ("article", "Article"),
        ("event", "Event"),
    ]

    POST_STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    content = models.TextField()
    file = models.FileField(upload_to="uploads/", blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    featured_image = models.ImageField(
        upload_to="featured_images/", blank=True, null=True
    )
    comments_count = models.PositiveIntegerField(default=0)
    # boolean
    comments_enabled = models.BooleanField(default=True)
    # choices
    status = models.CharField(
        max_length=20, choices=POST_STATUS_CHOICES, default="draft"
    )
    post_type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default="status"
    )
    privacy_settings = models.CharField(
        max_length=20, choices=PRIVACY_CHOICES, default="public"
    )
    # relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    # data-time
    scheduled_publish_time = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post #{self.pk} by {self.user.username}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment #{self.pk} on Post #{self.post.pk} by {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
