from .django_settings.databases import get_databases_settings
from .django_settings.installed_apps import get_installed_apps_settings
from .django_settings.middleware import get_middleware_settings
from .django_settings.templates import get_templates_settings
from .django_settings.auth_password_validators import (
    get_auth_password_validators_settings,
)

# third party settings
from .third_party_settings.django_rest_framework import (
    get_django_rest_framework_settings,
)

settings = {
    "db": get_databases_settings,
    "installed_apps": get_installed_apps_settings,
    "middleware": get_middleware_settings,
    "templates": get_templates_settings,
    "auth_password_validators": get_auth_password_validators_settings,
    # third party settings
    "rest_framework": get_django_rest_framework_settings,
}
