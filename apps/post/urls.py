from django.urls import path
from .views.api import post_views


urlpatterns = [
    path('', post_views.index),
    path('get_token/', post_views.get_csrf_token),
    path('create/', post_views.create_post)
]