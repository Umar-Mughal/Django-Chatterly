from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from apps.authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        unique=True, error_messages={"unique": "Email has been already been taken"}
    )
    password = models.CharField(max_length=128)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator],
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={"unique": "A user with that username already exists"},
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    # is_email_verified = models.BooleanField(default=False)
    # otp = models.CharField(max_length=6, null=True, blank=True)

    # phone_number = models.CharField(
    #     max_length=15,
    # )
    # date_of_birth = models.DateField()
    # GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # last_login = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
