from uuid import uuid4

from core.cast_member.application.usecase.get_cast_member_use_case import GetCastMemberUseCase, GetCastMemberInput
from core.cast_member.domain import CastMemberType, CastMember
from core.cast_member.infrastructure.mocks.cast_member_fake_repository import CastMemberFakeRepository


def test_when_cast_member_does_not_exist_then_return_none():
    cast_member_repository = CastMemberFakeRepository(cast_members=set())

    use_case = GetCastMemberUseCase(repository=cast_member_repository)
    request = GetCastMemberInput(cast_member_id=uuid4())
    response = use_case.execute(request)

    assert response.cast_member is None


def test_get_cast_member_by_id():
    cast_member = CastMember(id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)
    cast_member_2 = CastMember(id=uuid4(), name="Mary Stuart", cast_member_type=CastMemberType.DIRECTOR)
    cast_member_repository = CastMemberFakeRepository(cast_members={cast_member, cast_member_2})

    use_case = GetCastMemberUseCase(repository=cast_member_repository)
    request = GetCastMemberInput(cast_member_id=cast_member_2.id)
    response = use_case.execute(request)

    assert response.cast_member == cast_member_2
