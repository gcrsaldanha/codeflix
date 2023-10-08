from typing import Dict
from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from core.category.domain import Category
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


pytestmark = pytest.mark.django_db


@pytest.fixture(scope="function")
def category() -> Category:
    return Category(
        id=uuid4(),
        name="Category 1",
        description="Category 1 description",
        is_active=True,
    )


@pytest.fixture(scope="function", autouse=True)
def category_repository(category: Category) -> CategoryRepositoryInterface:
    category_repository = CategoryDjangoRepository()
    category_repository.create(category)
    return category_repository


class TestListCategoriesView:
    def test_list_categories(self, category: Category) -> None:
        api_client = APIClient()
        response = api_client.get("/api/categories/")

        assert response.status_code == 200
        assert response.data == [
            {
                "id": str(category.id),
                "name": "Category 1",
                "description": "Category 1 description",
                "is_active": True,
            }
        ]


class TestGetCategoryView:
    def test_return_category(self, category: Category) -> None:
        response = APIClient().get(f"/api/categories/{str(category.id)}/")

        assert response.status_code == 200
        assert response.data == {
            "id": str(category.id),
            "name": "Category 1",
            "description": "Category 1 description",
            "is_active": True,
        }

    def test_return_404_if_category_does_not_exist(self) -> None:
        category_id = uuid4()

        response = APIClient().get(f"/api/categories/{str(category_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": "Category not found"}

    def test_return_400_if_request_is_malformed(self) -> None:
        response = APIClient().get("/api/categories/invalid/")

        assert response.status_code == 400
        assert response.data == {"category_id": ["Must be a valid UUID."]}


class TestCreateCategoryView:
    def test_create_category_with_post_payload_data(self) -> None:
        response = APIClient().post(
            "/api/categories/",
            data={
                "name": "Category 1",
                "description": "Category 1 description",
            },
        )

        assert response.status_code == 201
        assert response.data == {"id": response.data["id"]}


class TestUpdateCategoryView:
    def test_when_category_exists_then_update_it(self, category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "id": str(category.id),
            "name": "Category 2",
            "description": "Category 2 description",
            "is_active": True,
        }

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        category_id = uuid4()

        response = APIClient().put(
            f"/api/categories/{str(category_id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"Category with id {category_id} does not exist"}

    def test_update_name_and_empty_description(self, category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "id": str(category.id),
            "name": "Category 2",
            "description": "",
            "is_active": True,
        }

    @pytest.mark.parametrize(
        "payload",
        [
            {"name": "Category 2"},
            {"description": "Category 2 description"},
            {},
        ],
    )
    def test_all_fields_keys_must_be_provided(self, payload: Dict[str, str], category: Category) -> None:
        response = APIClient().put(
            f"/api/categories/{str(category.id)}/",
            payload,
        )

        assert response.status_code == 400


class TestPartiallyUpdateCategoryView:
    def test_update_only_category_name(self, category: Category) -> None:
        response = APIClient().patch(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
            },
        )

        assert (response.status_code, response.data) == (
            200,
            {
                "id": str(category.id),
                "name": "Category 2",
                "description": "Category 1 description",
                "is_active": True,
            },
        )

    def test_update_only_category_description(self, category: Category) -> None:
        response = APIClient().patch(
            f"/api/categories/{str(category.id)}/",
            {
                "description": "Category 2 description",
            },
        )

        assert (response.status_code, response.data) == (
            200,
            {
                "id": str(category.id),
                "name": "Category 1",
                "description": "Category 2 description",
                "is_active": True,
            },
        )

    def test_update_name_and_description(self, category: Category) -> None:
        response = APIClient().patch(
            f"/api/categories/{str(category.id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
            },
        )

        assert response.status_code == 200
        assert response.data == {
            "id": str(category.id),
            "name": "Category 2",
            "description": "Category 2 description",
            "is_active": True,
        }

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        category_id = uuid4()

        response = APIClient().patch(
            f"/api/categories/{str(category_id)}/",
            {
                "name": "Category 2",
                "description": "Category 2 description",
            },
        )

        assert response.status_code == 404
        assert response.data == {"message": f"Category with id {category_id} does not exist"}


class TestDeleteCategory:
    def test_delete_category(self, category: Category) -> None:
        response = APIClient().delete(f"/api/categories/{str(category.id)}/")

        assert response.status_code == 204

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        category_id = uuid4()

        response = APIClient().delete(f"/api/categories/{str(category_id)}/")

        assert response.status_code == 404
        assert response.data == {"message": f"Category with id {category_id} does not exist"}
