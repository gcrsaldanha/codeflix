from uuid import uuid4

import pytest

from core.category.application.usecase.delete_category import DeleteCategoryRequest, DeleteCategory
from core.category.application.usecase.update_category import CategoryDoesNotExist
from core.category.domain import Category
from core.category.infrastructure.repositories.category_fake_repository import CategoryFakeRepository


def test_when_category_does_not_exist_then_raise_error():
    category_repository = CategoryFakeRepository(categories=set())

    delete_category = DeleteCategory(category_repository)
    request = DeleteCategoryRequest(category_id=uuid4())

    with pytest.raises(CategoryDoesNotExist, match=f"Category with id {request.category_id} does not exist"):
        delete_category.execute(request)


def test_delete_existing_category():
    category = Category(id=uuid4(), name="Drama", description="Category for drama")
    category_repository = CategoryFakeRepository(categories={category})
    assert category_repository.get_by_id(category.id) is not None

    delete_category = DeleteCategory(category_repository)
    request = DeleteCategoryRequest(category_id=category.id)
    response = delete_category.execute(request)

    assert response.category == category
    assert category_repository.get_by_id(category.id) is None
