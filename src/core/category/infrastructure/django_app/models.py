from uuid import uuid4

from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)  # TODO: Unique?
    description = models.TextField()
    is_active = models.BooleanField(default=True)
