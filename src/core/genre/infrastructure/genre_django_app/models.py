from typing import Set
from uuid import uuid4, UUID

from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    # TODO: here or in the repository?
    # @property
    # def category_ids(self) -> Set[UUID]:
    #     return {gc.category_id for gc in self.categories.all()}


class GenreCategory(models.Model):
    genre = models.ForeignKey("genre_django_app.Genre", related_name="related_categories", on_delete=models.CASCADE)
    category = models.ForeignKey("django_app.Category", related_name="related_genres", on_delete=models.CASCADE)
