from typing import Dict
from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.cast_member.domain import CastMember, CastMemberType


@pytest.mark.django_db
class TestUpdateCastMemberView:
    def test_when_cast_member_exists_then_update_it(self, actor: CastMember) -> None:
        response = APIClient().put(
            f"/api/cast_members/{str(actor.id)}/",
            {
                "name": "Johnny Doe",
                "cast_member_type": "DIRECTOR",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(actor.id),
                "name": "Johnny Doe",
                "cast_member_type": "DIRECTOR",
            }
        }

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        cast_member_id = uuid4()

        response = APIClient().put(
            f"/api/cast_members/{str(cast_member_id)}/",
            {
                "name": "Johnny Doe",
                "cast_member_type": "DIRECTOR",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"CastMember with id {cast_member_id} does not exist"}

    def test_update_name_and_type(self, actor: CastMember) -> None:
        response = APIClient().put(
            f"/api/cast_members/{str(actor.id)}/",
            {
                "name": "Jonny Doe",
                "cast_member_type": "DIRECTOR",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "data": {
                "id": str(actor.id),
                "name": "Jonny Doe",
                "cast_member_type": "DIRECTOR",
            }
        }

    @pytest.mark.parametrize(
        "payload",
        [
            {"name": "Johnny Doe"},
            {"cast_member_type": "DIRECTOR"},
        ],
    )
    def test_all_fields_keys_must_be_provided(self, payload: Dict[str, str], actor: CastMember) -> None:
        response = APIClient().put(
            f"/api/cast_members/{str(actor.id)}/",
            payload,
        )

        assert response.status_code == 400
