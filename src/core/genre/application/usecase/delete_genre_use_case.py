from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.genre.application.usecase.exceptions import GenreDoesNotExist
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.repositories import GenreDjangoRepository


@dataclass
class DeleteGenreInput:
    genre_id: UUID


@dataclass
class DeleteGenreOutput:
    genre: Genre


class DeleteGenreUseCase(UseCase[DeleteGenreInput, DeleteGenreOutput]):
    def __init__(self, repository: Optional[GenreRepositoryInterface] = None):
        self._repository = repository or GenreDjangoRepository()

    def execute(self, request: DeleteGenreInput) -> DeleteGenreOutput:
        genre = self._repository.get_by_id(request.genre_id)
        if genre is None:
            raise GenreDoesNotExist(f"Genre with id {request.genre_id} does not exist")

        self._repository.delete(genre.id)

        return DeleteGenreOutput(genre)
