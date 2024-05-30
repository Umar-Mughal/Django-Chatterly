from django.urls import path, include
from apps.post.views.api import post_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", post_view.PostViewSet)
urlpatterns = [
    path("/upload/", post_view.UploadPost.as_view()),
    # path("/upload/", post_view.upload_post),
    path("/", include(router.urls)),
]
