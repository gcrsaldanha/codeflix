from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.category.domain import Category


@pytest.mark.django_db
class TestDeleteCategory:
    def test_delete_category(self, category: Category) -> None:
        response = APIClient().delete(f"/api/categories/{str(category.id)}/")

        assert response.status_code == 204

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        category_id = uuid4()

        response = APIClient().delete(f"/api/categories/{str(category_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": f"Category with id {category_id} does not exist"}
