from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.cast_member.domain import CastMember


@pytest.mark.django_db
class TestPartiallyUpdateCastMemberView:
    def test_update_only_cast_member_name(self, actor: CastMember) -> None:
        response = APIClient().patch(
            f"/api/cast_members/{str(actor.id)}/",
            {
                "name": "Johnny Doe",
            },
        )

        assert (response.status_code, response.data) == (
            200,
            {
                "data": {
                    "id": str(actor.id),
                    "name": "Johnny Doe",
                    "cast_member_type": "ACTOR",
                }
            },
        )

    def test_update_only_cast_member_type(self, actor: CastMember) -> None:
        response = APIClient().patch(
            f"/api/cast_members/{str(actor.id)}/",
            {
                "cast_member_type": "DIRECTOR",
            },
        )

        assert (response.status_code, response.data) == (
            200,
            {
                "data": {
                    "id": str(actor.id),
                    "name": actor.name,
                    "cast_member_type": "DIRECTOR",
                },
            },
        )

    def test_update_name_and_type(self, actor: CastMember) -> None:
        response = APIClient().patch(
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

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        cast_member_id = uuid4()

        response = APIClient().patch(
            f"/api/cast_members/{str(cast_member_id)}/",
            {
                "name": "Johnny Doe",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"CastMember with id {cast_member_id} does not exist"}
