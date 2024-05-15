from rest_framework.authentication import BaseAuthentication


class NoAuthentication(BaseAuthentication):
    """
    No authentication.
    """

    def authenticate(self, request):
        # Always return None to indicate no authentication was performed
        return None

    def has_permission(self, request, view):
        # Always return True to indicate permission is granted
        return True
