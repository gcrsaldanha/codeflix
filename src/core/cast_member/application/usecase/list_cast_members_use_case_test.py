from uuid import uuid4

import pytest

from core.cast_member.application.usecase.list_cast_members_use_case import (
    ListCastMembersInput,
    ListCastMembersUseCase,
)
from core.cast_member.domain.entity.cast_member import CastMember, CastMemberType
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.mocks.cast_member_fake_repository import CastMemberFakeRepository


@pytest.fixture
def cast_actor() -> CastMember:
    return CastMember(id=uuid4(), name="John Doe", cast_member_type=CastMemberType.ACTOR)


@pytest.fixture
def cast_actor_2() -> CastMember:
    return CastMember(id=uuid4(), name="Zack Doe", cast_member_type=CastMemberType.ACTOR)


@pytest.fixture
def cast_director() -> CastMember:
    return CastMember(id=uuid4(), name="Mary Stuart", cast_member_type=CastMemberType.DIRECTOR)


@pytest.fixture
def repository(cast_actor, cast_director, cast_actor_2) -> CastMemberRepositoryInterface:
    repo = CastMemberFakeRepository(
        cast_members={
            cast_actor,
            cast_director,
            cast_actor_2,
        }
    )
    return repo


def test_list_cast_members_ordered_by_name_page_one(
    repository,
    cast_actor,
    cast_director,
):
    use_case = ListCastMembersUseCase(repository=repository)
    paginated_request = ListCastMembersInput(
        page=1,
        page_size=2,
    )
    response = use_case.execute(paginated_request)

    assert response.data == [
        cast_actor,
        cast_director,
    ]
    assert response.meta.next_page == 2
    assert response.meta.page == 1
    assert response.meta.total_quantity == 3


def test_list_cast_members_ordered_by_name_page_two(
    repository,
    cast_actor,
    cast_director,
    cast_actor_2,
):
    use_case = ListCastMembersUseCase(repository=repository)
    paginated_request = ListCastMembersInput(
        page=2,
        page_size=2,
    )
    response = use_case.execute(paginated_request)
    assert response.data == [
        cast_actor_2,
    ]
    assert response.meta.next_page is None
    assert response.meta.page == 2
    assert response.meta.total_quantity == 3


def test_list_directors_only(
    repository,
    cast_director,
):
    use_case = ListCastMembersUseCase(repository=repository)
    paginated_request = ListCastMembersInput(
        page=1,
        page_size=2,
        filters={"cast_member_type": CastMemberType.DIRECTOR},
    )
    response = use_case.execute(paginated_request)
    assert response.data == [
        cast_director,
    ]
    assert response.meta.next_page is None
    assert response.meta.page == 1
    assert response.meta.total_quantity == 1
