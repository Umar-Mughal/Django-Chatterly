from django.urls import path, include
from apps.user.views.api.user_view import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", UserViewSet)
urlpatterns = [
    path("/", include(router.urls)),
    # path(
    #     "/account",
    #     UserViewSet.get_account({"get": "get_account"}),
    # ),
]
