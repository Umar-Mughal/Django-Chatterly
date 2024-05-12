from datetime import timedelta


def rest_framework():
    return {
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        )
    }


def simple_jwt():
    return {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    }
