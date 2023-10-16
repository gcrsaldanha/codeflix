from uuid import uuid4

import pytest

from core.cast_member.application.usecase.update_cast_member_use_case import (
    UpdateCastMemberUseCase,
    UpdateCastMemberInput,
)
from core.cast_member.application.usecase.exceptions import CastMemberDoesNotExist
from core.cast_member.domain import CastMember, CastMemberType
from core.cast_member.infrastructure.mocks.cast_member_fake_repository import CastMemberFakeRepository


def test_when_cast_member_does_not_exist_then_raises_exception():
    request = UpdateCastMemberInput(cast_member_id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)
    repository = CastMemberFakeRepository(cast_members=set())

    use_case = UpdateCastMemberUseCase(repository=repository)

    with pytest.raises(CastMemberDoesNotExist, match=f"CastMember with id {request.cast_member_id} does not exist"):
        use_case.execute(request)


def test_update_cast_member_name_only():
    existing_cast_member = CastMember(id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)
    repository = CastMemberFakeRepository(cast_members={existing_cast_member})

    request = UpdateCastMemberInput(cast_member_id=existing_cast_member.id, name="John Doe 2")
    use_case = UpdateCastMemberUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.cast_member.id == existing_cast_member.id
    assert response.cast_member.name == "John Doe 2"
    assert response.cast_member.cast_member_type == CastMemberType.ACTOR


def test_update_cast_member_type_only():
    existing_cast_member = CastMember(id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)
    repository = CastMemberFakeRepository(cast_members={existing_cast_member})

    request = UpdateCastMemberInput(cast_member_id=existing_cast_member.id, cast_member_type=CastMemberType.DIRECTOR)
    use_case = UpdateCastMemberUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.cast_member.id == existing_cast_member.id
    assert response.cast_member.name == "John Doe"
    assert response.cast_member.cast_member_type == CastMemberType.DIRECTOR


def test_update_cast_member_name_and_type():
    existing_cast_member = CastMember(id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)
    repository = CastMemberFakeRepository(cast_members={existing_cast_member})

    request = UpdateCastMemberInput(
        cast_member_id=existing_cast_member.id,
        name="John Doe 2",
        cast_member_type=CastMemberType.DIRECTOR,
    )
    use_case = UpdateCastMemberUseCase(repository=repository)
    response = use_case.execute(request)

    assert response.cast_member.id == existing_cast_member.id
    assert response.cast_member.name == "John Doe 2"
    assert response.cast_member.cast_member_type == CastMemberType.DIRECTOR
