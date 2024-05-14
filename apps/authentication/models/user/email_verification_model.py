from django.db import models
from apps.authentication.models import User


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True, blank=True)
    sent_at = models.DateTimeField()
