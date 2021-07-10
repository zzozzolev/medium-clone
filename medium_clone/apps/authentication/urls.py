from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView

urlpatterns = [
    url(r"^register/", RegisterView.as_view(), name="register"),
    url(r"^get-auth-token/", obtain_auth_token, name="get-auth-token")
]
