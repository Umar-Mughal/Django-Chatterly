from django.db import models
from django.contrib.auth.models import User


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
    comments_enabled = models.BooleanField(default=True)
    privacy_settings = models.CharField(
        max_length=20, choices=PRIVACY_CHOICES, default="public"
    )
    is_hidden = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    has_poll = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    poll_question = models.CharField(max_length=255, blank=True, null=True)
    original_post = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    event = models.ForeignKey("Event", on_delete=models.SET_NULL, blank=True, null=True)
    scheduled_publish_time = models.DateTimeField(blank=True, null=True)
    reactions = models.ManyToManyField("Reaction", through="PostReaction")
    post_type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default="status"
    )
    views_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    reach_count = models.PositiveIntegerField(default=0)
    featured_image = models.ImageField(
        upload_to="featured_images/", blank=True, null=True
    )
    expiry_date = models.DateTimeField(blank=True, null=True)
    target_age_group = models.CharField(max_length=20, blank=True, null=True)
    target_location = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=POST_STATUS_CHOICES, default="draft"
    )
    is_promoted = models.BooleanField(default=False)

    score = models.FloatField(default=0.0)
    source = models.CharField(max_length=50, blank=True, null=True)
    context = models.CharField(max_length=100, blank=True, null=True)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    target_interests = models.ManyToManyField("Interest", blank=True)
    co_authors = models.ManyToManyField(
        User, related_name="co_authored_posts", blank=True
    )

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


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.name


class Reaction(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
