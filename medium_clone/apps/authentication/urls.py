from django.conf.urls import include, url

from .views import RegisterView

urlpatterns = [
    url(r"^register/", RegisterView.as_view())
]
