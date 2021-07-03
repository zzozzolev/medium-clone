from django.db import models

from apps.common.models import Timestamped


class Profile(Timestamped):
    user = models.OneToOneField(
        "auth.User", related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("user__username", )
