from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.genre.domain import Genre
from core.genre.infrastructure.genre_django_app.repositories import (
    GenreRepositoryInterface,
    GenreDjangoRepository,
)


@dataclass
class GetGenreInput:
    genre_id: UUID


@dataclass
class GetGenreOutput:
    genre: Optional[Genre]


class GetGenreUseCase(UseCase[GetGenreInput, GetGenreOutput]):
    def __init__(self, repository: Optional[GenreRepositoryInterface] = None):
        self._repository = repository or GenreDjangoRepository()

    def execute(self, request: GetGenreInput) -> GetGenreOutput:
        genre = self._repository.get_by_id(request.genre_id)
        return GetGenreOutput(genre)
