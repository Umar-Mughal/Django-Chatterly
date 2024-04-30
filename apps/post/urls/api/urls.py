from django.urls import path
from ...views.api import post_view


urlpatterns = [
    # CRATE POST
    path("", post_view.create_post),
]
