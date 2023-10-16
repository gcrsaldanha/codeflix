from uuid import uuid4

import pytest

from core.cast_member.application.usecase.delete_cast_member_use_case import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)
from core.cast_member.application.usecase.exceptions import CastMemberDoesNotExist
from core.cast_member.domain import CastMember, CastMemberType
from core.cast_member.infrastructure.mocks.cast_member_fake_repository import CastMemberFakeRepository


def test_when_cast_member_does_not_exist_then_raise_error():
    repository = CastMemberFakeRepository(cast_members=set())

    delete_cast_member = DeleteCastMemberUseCase(repository)
    request = DeleteCastMemberInput(cast_member_id=uuid4())

    with pytest.raises(CastMemberDoesNotExist, match=f"CastMember with id {request.cast_member_id} does not exist"):
        delete_cast_member.execute(request)


def test_delete_existing_cast_member():
    cast_member = CastMember(id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)
    repository = CastMemberFakeRepository(cast_members={cast_member})
    assert repository.get_by_id(cast_member.id) is not None

    delete_cast_member = DeleteCastMemberUseCase(repository)
    request = DeleteCastMemberInput(cast_member_id=cast_member.id)
    response = delete_cast_member.execute(request)

    assert response.cast_member == cast_member
    assert repository.get_by_id(cast_member.id) is None
