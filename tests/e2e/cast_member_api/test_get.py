from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.cast_member.domain import CastMember


@pytest.mark.django_db
class TestGetCastMemberView:
    def test_return_cast_member(self, actor: CastMember) -> None:
        response = APIClient().get(f"/api/cast_members/{str(actor.id)}/")

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(actor.id),
                "name": actor.name,
                "cast_member_type": actor.cast_member_type.name,
            },
        }

    def test_return_404_if_cast_member_does_not_exist(self) -> None:
        cast_member_id = uuid4()

        response = APIClient().get(f"/api/cast_members/{str(cast_member_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": "CastMember not found"}

    def test_return_400_if_request_is_malformed(self) -> None:
        response = APIClient().get("/api/cast_members/invalid/")

        assert response.status_code == 400
        assert response.data == {"cast_member_id": ["Must be a valid UUID."]}
