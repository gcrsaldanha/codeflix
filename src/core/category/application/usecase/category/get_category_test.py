from uuid import uuid4

from core.category.application.usecase.category.get_category import GetCategoryRequest, GetCategory
from core.category.domain import Category
from core.category.infrastructure.repositories.category_fake_repository import CategoryFakeRepository


def test_when_category_does_not_exist_then_return_none():
    category_repository = CategoryFakeRepository(categories=set())

    use_case = GetCategory(category_repository=category_repository)
    request = GetCategoryRequest(category_id=uuid4())
    response = use_case.execute(request)

    assert response.category is None


def test_get_category_by_id():
    category = Category(id=uuid4(), name="Drama", description="Category for drama")
    category_2 = Category(id=uuid4(), name="Action", description="Category for action")
    category_repository = CategoryFakeRepository(categories={category, category_2})

    use_case = GetCategory(category_repository=category_repository)
    request = GetCategoryRequest(category_id=category_2.id)
    response = use_case.execute(request)

    assert response.category == category_2
