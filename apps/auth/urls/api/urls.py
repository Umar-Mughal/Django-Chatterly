from django.urls import path
from ...views.api import token_view


urlpatterns = [
    path("get_token/", token_view.get_csrf_token),
]
