from dataclasses import dataclass
from typing import Optional, Set
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
    categories: Set[Category]  # TODO: is it ok for the application layer to know about category domain?

    def validate(self):
        pass


@dataclass
class CreateGenreOutput:
    id: UUID


class CreateGenreUseCase(UseCase[CreateGenreInput, CreateGenreOutput]):
    def __init__(self, repository: Optional[GenreRepositoryInterface] = None):
        self._repository = repository or GenreDjangoRepository()

    def execute(self, request: CreateGenreInput) -> CreateGenreOutput:
        # TODO: should this fetch the Category objects from the repository?
        entity = Genre(
            name=request.name,
            description=request.description,
            categories={category_id for category_id in request.categories},
        )

        self._repository.create(entity)

        return CreateGenreOutput(id=entity.id)
