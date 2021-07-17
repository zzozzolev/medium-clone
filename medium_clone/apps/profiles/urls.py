from django.urls import path

from .views import ProfileRetrieveView

urlpatterns = [
    path("profiles/<str:username>/",
         ProfileRetrieveView.as_view(), name="profile_retrieve_view")
]
