from django.contrib.auth.models import BaseUserManager

"""
CUSTOM USER MANAGER
"""


class UserManager(BaseUserManager):
    def create_user(self, data):
        email = data.pop("email")
        email = self.normalize_email(email)
        password = data.pop("password")

        user = self.model(email=email, **data)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, data):
        data.setdefault("is_staff", True)
        data.setdefault("is_superuser", True)

        if data.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if data.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(data)
