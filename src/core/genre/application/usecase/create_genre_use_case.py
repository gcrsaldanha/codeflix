from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.category.domain import Category
from core.genre.domain.entity.genre import Genre
from core.genre.infrastructure.genre_django_app.repositories import (
    GenreRepositoryInterface,
    GenreDjangoRepository,
)


@dataclass
class CreateGenreInput:
    name: str
    description: str
    categories: List[Category]

    def validate(self):
        pass


@dataclass
class CreateGenreOutput:
    id: UUID


class CreateGenreUseCase(UseCase[CreateGenreInput, CreateGenreOutput]):
    def __init__(self, repository: Optional[GenreRepositoryInterface] = None):
        self._repository = repository or GenreDjangoRepository()

    def execute(self, request: CreateGenreInput) -> CreateGenreOutput:
        entity = Genre(name=request.name, description=request.description, categories=request.categories)

        self._repository.create(entity)

        return CreateGenreOutput(id=entity.id)
