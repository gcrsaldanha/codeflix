from unittest.mock import create_autospec

import pytest

from core.cast_member.application.usecase.create_cast_member_use_case import (
    CreateCastMemberInput,
    CreateCastMemberUseCase,
)
from core.cast_member.domain import CastMemberType
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface


class TestCreateCastMemberUseCase:
    @pytest.fixture
    def repository(self) -> CastMemberRepositoryInterface:
        return create_autospec(CastMemberRepositoryInterface)

    def test_create_cast_member_with_valid_data(self, repository: CastMemberRepositoryInterface):
        request = CreateCastMemberInput(name="John Doe", cast_member_type=CastMemberType.ACTOR)
        use_case = CreateCastMemberUseCase(repository=repository)

        response = use_case.execute(request)

        assert response.id
        assert repository.create.called
        assert repository.get_by_id(response.id)
