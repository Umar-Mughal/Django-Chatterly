from .django_settings import (
    databases,
    installed_apps,
    middleware,
    templates,
    auth_password_validators,
)

# third party settings
from .third_party_settings import rest_framework, simple_jwt

settings = {
    "databases": databases,
    "installed_apps": installed_apps,
    "middleware": middleware,
    "templates": templates,
    "auth_password_validators": auth_password_validators,
    # third party settings
    "rest_framework": rest_framework,
    "simple_jwt": simple_jwt,
}
