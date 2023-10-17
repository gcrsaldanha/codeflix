import pytest
from rest_framework.test import APIClient

from core.cast_member.domain import CastMemberType


@pytest.mark.django_db
class TestCreateCastMemberView:
    def test_create_cast_member_with_post_payload_data(self) -> None:
        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": "John Doe",
                "cast_member_type": "ACTOR",
            },
        )

        assert response.status_code == 201
        assert response.data == {"id": response.data["id"]}
