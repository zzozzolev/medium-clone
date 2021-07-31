from django.db import models

from apps.common.models import Timestamped


class Post(Timestamped):
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name='posts')
    # max_length=300 is heuristics.
    title = models.CharField(db_index=True, max_length=300)
    # slug field is used to api apth, so it should be unique.
    slug = models.SlugField(db_index=True, max_length=300, unique=True)
    body = models.TextField()
    description = models.TextField()
