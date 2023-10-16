from uuid import uuid4

import pytest

from core.cast_member.domain import CastMember, CastMemberType
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberDjangoRepository


@pytest.fixture(scope="function")
def actor() -> CastMember:
    return CastMember(
        id=uuid4(),
        name="John Actor",
        cast_member_type=CastMemberType.ACTOR,
    )


@pytest.fixture(scope="function")
def director() -> CastMember:
    return CastMember(
        id=uuid4(),
        name="Mary Director",
        cast_member_type=CastMemberType.DIRECTOR,
    )


@pytest.fixture(scope="function", autouse=True)
def cast_member_repository(actor: CastMember, director: CastMember) -> CastMemberRepositoryInterface:
    repository = CastMemberDjangoRepository()
    repository.create(actor)
    repository.create(director)
    return repository
