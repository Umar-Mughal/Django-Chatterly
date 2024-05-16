# Packages
import re
from django.contrib.auth.hashers import check_password

# Models
from apps.authentication.models import User


class UserUtil:
    @staticmethod
    def generate_unique_username(email):
        # Use email prefix as username
        username = email.split("@")[0]
        # Ensure username is unique
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{username}_{suffix}"
            suffix += 1
        return username

    @classmethod
    def is_strong_password(cls, password):
        return True
        # Define regex pattern for strong password requirements
        pattern = (
            r"^(?=.*[A-Z])"  # At least one uppercase letter
            r"(?=.*[a-z])"  # At least one lowercase letter
            r"(?=.*\d)"  # At least one digit
            r"(?=.*[@$!%*#?&])"  # At least one special character
            r".{8,}$"  # At least 8 characters long
        )

        # Check if password matches the regex pattern
        return bool(re.match(pattern, password))

    @staticmethod
    def validate_password(self, data):
        err = {"status": False, "msg": ""}
        # If change password flow, then check old password validation
        if "old_password" in data:
            old_password = data["old_password"]
            user = self.context["request"].user
            if not check_password(old_password, user.password):
                err["status"] = True
                err["msg"] = "Old password is incorrect"
                return err

        # --- Now check further common validations ---- #
        # 1. Check if passwords match
        password = data["password"]
        password_confirm = data["password_confirm"]
        if password != password_confirm:
            err["status"] = True
            err["msg"] = "Passwords do not match."

        # 2. Check if password meets strength requirements
        if not UserUtil.is_strong_password(password):
            err["status"] = True
            err["msg"] = (
                "Password must be 8 characters long and contain at least one upper case letter, one lowercase letter, one digit, and one special character."
            )
        return err
