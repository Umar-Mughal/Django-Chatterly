from django.urls import path, include
from ...views.api import post_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"posts", post_view.PostViewSet)

urlpatterns = [path("", include(router.urls))]

# urlpatterns = [
#     # CRATE POST
#     # path("", post_view.create_post_function),
#     # path("", post_view.PostCreateAPIViewClass.as_view()),
#     # path("", post_view.PostCreateCreateAPIViewClass.as_view()),
#     # path(
#     #     "",
#     #     post_view.PostViewSet.as_view(
#     #         {
#     #             "post": "create",  # Maps the HTTP POST method to the 'create' action
#     #         }
#     #     ),
#     # ),
#     path(
#         "",
#         post_view.PostViewSet.as_view(),
#     )
# ]
