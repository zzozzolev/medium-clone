from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, PostLikeAPIView

# By default the URLs created by DefaultRouter are appended with a trailing slash.
router = DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("posts/<str:slug>/like/", PostLikeAPIView.as_view(), name="post_like_view")
]
