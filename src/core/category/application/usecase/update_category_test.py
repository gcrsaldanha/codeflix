from uuid import uuid4

import pytest

from core.category.application.usecase.update_category import UpdateCategory, UpdateCategoryRequest, \
    CategoryDoesNotExist
from core.category.domain import Category
from core.category.infrastructure.repositories.category_fake_repository import CategoryFakeRepository


def test_when_category_does_not_exist_then_raises_exception():
    request = UpdateCategoryRequest(category_id=uuid4(), name="Drama", description="Category for drama")
    category_repository = CategoryFakeRepository(categories=set())

    use_case = UpdateCategory(category_repository=category_repository)

    with pytest.raises(CategoryDoesNotExist, match=f"Category with id {request.category_id} does not exist"):
        use_case.execute(request)


def test_update_category_name_only():
    existing_category = Category(id=uuid4(), name="Drama", description="Category for drama")
    category_repository = CategoryFakeRepository(categories={existing_category})

    request = UpdateCategoryRequest(category_id=existing_category.id, name="Comedy")
    use_case = UpdateCategory(category_repository=category_repository)
    response = use_case.execute(request)

    assert response.category.id == existing_category.id
    assert response.category.name == "Comedy"
    assert response.category.description == "Category for drama"


def test_update_category_description_only():
    existing_category = Category(id=uuid4(), name="Drama", description="Category for drama")
    category_repository = CategoryFakeRepository(categories={existing_category})

    request = UpdateCategoryRequest(category_id=existing_category.id, description="Category for comedy")
    use_case = UpdateCategory(category_repository=category_repository)
    response = use_case.execute(request)

    assert response.category.id == existing_category.id
    assert response.category.name == "Drama"
    assert response.category.description == "Category for comedy"


def test_update_category_name_and_description():
    existing_category = Category(id=uuid4(), name="Drama", description="Category for drama")
    category_repository = CategoryFakeRepository(categories={existing_category})

    request = UpdateCategoryRequest(category_id=existing_category.id, name="Comedy", description="Category for comedy")
    use_case = UpdateCategory(category_repository=category_repository)
    response = use_case.execute(request)

    assert response.category.id == existing_category.id
    assert response.category.name == "Comedy"
    assert response.category.description == "Category for comedy"
