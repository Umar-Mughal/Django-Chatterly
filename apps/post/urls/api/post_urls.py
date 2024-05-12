from django.urls import path, include
from apps.post.views.api.post_view import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", PostViewSet)
urlpatterns = [path("/", include(router.urls))]
