from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.genre.application.usecase.exceptions import UpdateGenreException, GenreDoesNotExist
from core.genre.domain import Genre
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface
from core.genre.infrastructure.genre_django_app.repositories import GenreDjangoRepository


@dataclass
class UpdateGenreInput:
    genre_id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    # TODO: updating categories of a genre as a separate usecase?


@dataclass
class UpdateGenreOutput:
    genre: Genre


class UpdateGenreUseCase(UseCase[UpdateGenreInput, UpdateGenreOutput]):
    def __init__(self, repository: Optional[GenreRepositoryInterface] = None):
        self._repository = repository or GenreDjangoRepository()

    def execute(self, request: UpdateGenreInput) -> UpdateGenreOutput:
        genre = self._repository.get_by_id(request.genre_id)
        if genre is None:
            raise GenreDoesNotExist(f"Genre with id {request.genre_id} does not exist")

        # Only update fields that are provided
        if request.name is None:
            request.name = genre.name

        if request.description is None:
            request.description = genre.description

        # Activating/deactivating genre as a "separate" action on the domain object
        # If we want, we could extract this to another usecase
        if request.is_active is None:
            request.is_active = genre.is_active
        else:
            if request.is_active:
                genre.activate()
            else:
                genre.deactivate()

        genre.change_genre(request.name, request.description)  # TODO: monads / result
        if genre.notification.has_errors():
            raise UpdateGenreException(genre.notification.errors)

        self._repository.update(genre)

        return UpdateGenreOutput(genre)
