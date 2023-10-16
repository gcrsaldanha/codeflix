import pytest
from rest_framework.test import APIClient

from core.cast_member.domain import CastMember, CastMemberType


@pytest.mark.django_db
class TestListCastMembersView:
    def test_list_cast_members(self, actor: CastMember, director: CastMember) -> None:
        api_client = APIClient()
        response = api_client.get("/api/cast_members/")

        assert response.status_code == 200
        assert response.data == {
            "data": [
                {
                    "id": str(actor.id),
                    "name": actor.name,
                    "cast_member_type": CastMemberType.ACTOR.name,
                },
                {
                    "id": str(director.id),
                    "name": director.name,
                    "cast_member_type": CastMemberType.DIRECTOR.name,
                },
            ],
            "meta": {
                "next_page": None,
                "page": 1,
                "page_size": 2,
                "total_quantity": 2,
            },
        }

    def test_list_cast_members_with_pagination(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        api_client = APIClient()
        response = api_client.get("/api/cast_members/?page=1&page_size=1")

        assert response.data == {
            "data": [
                {
                    "id": str(actor.id),
                    "name": actor.name,
                    "cast_member_type": CastMemberType.ACTOR.name,
                },
            ],
            "meta": {
                "next_page": 2,
                "page": 1,
                "page_size": 1,
                "total_quantity": 2,
            },
        }
        assert response.status_code == 200
