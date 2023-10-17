from unittest.mock import create_autospec

import pytest

from core.category.domain import Category
from core.genre.application.usecase.create_genre_use_case import (
    CreateGenreInput,
    CreateGenreUseCase,
)
from core.genre.domain.repository.genre_repository_interface import GenreRepositoryInterface


class TestCreateGenreUseCase:
    @pytest.fixture
    def repository(self) -> GenreRepositoryInterface:
        return create_autospec(GenreRepositoryInterface)

    def test_create_genre_with_valid_data(self, repository: GenreRepositoryInterface):
        category = Category(name="Category 1", description="Category 1 description")
        request = CreateGenreInput(name="Genre 1", description="Genre 1 description", categories=[category])
        use_case = CreateGenreUseCase(repository=repository)

        response = use_case.execute(request)

        assert response.id
        assert repository.create.called
        assert repository.get_by_id(response.id)
