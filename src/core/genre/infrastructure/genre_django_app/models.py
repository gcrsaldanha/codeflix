from typing import List
from uuid import uuid4

from django.db import models

from core.category.domain import Category


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    @property
    def categories(self) -> List[Category]:
        # TODO: this is a placeholder
        return [Category(name="Category 1", description="Category 1 description", is_active=True)]
