from uuid import uuid4

from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class GenreCategory(models.Model):
    genre = models.ForeignKey("genre_django_app.Genre", on_delete=models.CASCADE)
    category = models.ForeignKey("django_app.Category", on_delete=models.CASCADE)
