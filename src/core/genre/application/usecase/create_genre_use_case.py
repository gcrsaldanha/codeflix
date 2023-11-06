from dataclasses import dataclass
from typing import Optional, Set
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.genre.domain.entity.genre import Genre
from core.genre.infrastructure.genre_django_app.repositories import (
    GenreRepositoryInterface,
    GenreDjangoRepository,
)


@dataclass
class CreateGenreInput:
    name: str
    description: str
    categories: Set[UUID]

    def validate(self):
        pass


@dataclass
class CreateGenreOutput:
    id: UUID


class CreateGenreUseCase(UseCase[CreateGenreInput, CreateGenreOutput]):
    def __init__(
        self,
        repository: Optional[GenreRepositoryInterface] = None,
        category_repository: Optional[CategoryRepositoryInterface] = None,
    ):
        self._repository = repository or GenreDjangoRepository()
        self._category_repository = category_repository or CategoryDjangoRepository()

    def execute(self, request: CreateGenreInput) -> CreateGenreOutput:
        entity = Genre(
            name=request.name,
            description=request.description,
            categories={category_id for category_id in request.categories},
        )

        self._repository.create(entity)

        return CreateGenreOutput(id=entity.id)
