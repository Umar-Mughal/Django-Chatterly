from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from apps.authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # First name
    first_name = models.CharField(max_length=150)
    # Last name
    last_name = models.CharField(max_length=150)
    # Gender
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # Date of birth
    date_of_birth = models.DateField()
    # Email
    email = models.EmailField(
        unique=True, error_messages={"unique": "Email has been already been taken"}
    )
    # Password
    password = models.CharField(max_length=128)
    """OTHER FIELDS: ON"""
    # Username
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
    is_email_verified = models.BooleanField(default=False)

    # phone_number = models.CharField(
    #     max_length=15,
    # )
    # last_login = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
