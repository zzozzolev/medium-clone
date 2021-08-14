from django.db import models

from apps.common.models import Timestamped


class Post(Timestamped):
    # The reason it uses Profile for FK instead of User is that Profile will display related posts.
    # It is likely to be unconfortable if Post relates with User.
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name='posts')
    # max_length=300 is heuristics.
    title = models.CharField(db_index=True, max_length=300)
    # slug field is used to api apth, so it should be unique.
    slug = models.SlugField(db_index=True, max_length=300, unique=True)
    body = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title
