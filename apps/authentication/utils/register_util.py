# Models
from apps.authentication.models import User


class RegisterUtil:
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
