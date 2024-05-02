def get_installed_apps_settings():
    return [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # third party apps
        "rest_framework",
        "django_extensions",
        # custom apps
        "apps.post",
        "apps.custom_auth",
    ]
