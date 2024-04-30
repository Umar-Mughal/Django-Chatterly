from django.db import models
from django.contrib.auth.models import User
from .tag_model import Tag


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
    post_url = models.URLField(blank=True)
    location = models.CharField(
        max_length=255,
        blank=True,
    )
    featured_image = models.ImageField(
        upload_to="featured_images/", blank=True, null=True
    )
    # boolean
    comments_enabled = models.BooleanField(default=True)
    # choices
    post_type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default="status"
    )
    privacy_settings = models.CharField(
        max_length=20, choices=PRIVACY_CHOICES, default="public"
    )
    status = models.CharField(
        max_length=20, choices=POST_STATUS_CHOICES, default="draft"
    )
    # relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    # data-time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post #{self.pk} by {self.user.username}"
