from django.db import models
from apps.authentication.models import User


class EmailVerification(models.Model):
    EMAIL_TYPES = {
        "register": "register",
        "reset_password": "reset_password",
    }
    EMAIL_TYPE_CHOICES = [
        (EMAIL_TYPES["register"], "Register Email Verification"),
        (EMAIL_TYPES["reset_password"], "Reset Password"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_type = models.CharField(
        max_length=50, null=True, blank=True, choices=EMAIL_TYPE_CHOICES
    )
    code = models.CharField(max_length=6, null=True, blank=True)
    sent_at = models.DateTimeField()

    class Meta:
        unique_together = ("user", "email_type", "code")
