from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet

# By default the URLs created by DefaultRouter are appended with a trailing slash.
router = DefaultRouter()
router.register(r"posts", PostViewSet)

urlpatterns = router.urls
