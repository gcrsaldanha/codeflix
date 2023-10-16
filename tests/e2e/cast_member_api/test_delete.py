from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.cast_member.domain import CastMember, CastMemberType


@pytest.mark.django_db
class TestDeleteCastMemberView:
    def test_delete_cast_member(self, actor: CastMember) -> None:
        response = APIClient().delete(f"/api/cast_members/{str(actor.id)}/")

        assert response.status_code == 204

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        cast_member_id = uuid4()

        response = APIClient().delete(f"/api/cast_members/{str(cast_member_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": f"CastMember with id {cast_member_id} does not exist"}
