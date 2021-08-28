from django.db import models


class Timestamped(models.Model):
    # Automatically set the field to now every time the object is saved.
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically set the field to now when the object is first created.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
