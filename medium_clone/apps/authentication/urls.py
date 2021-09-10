from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("jwt/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]
