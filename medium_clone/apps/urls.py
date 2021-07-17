from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("api/", include("apps.authentication.urls")),
    path("api/", include("apps.profiles.urls"))
]
