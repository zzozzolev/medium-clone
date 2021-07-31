from django.urls import path

from .views import ProfileRetrieveUpdateAPIView

urlpatterns = [
    path("profiles/<str:username>/",
         ProfileRetrieveUpdateAPIView.as_view(), name="profile_retrieveupdate_view")
]
