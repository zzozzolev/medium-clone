from django.db import models

from apps.common.models import Timestamped


class Profile(Timestamped):
    user = models.OneToOneField(
        "auth.User", related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    liked_posts = models.ManyToManyField(
        "posts.Post", related_name="liked_authors")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("user__username", )
