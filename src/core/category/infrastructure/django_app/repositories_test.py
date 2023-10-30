import pytest
from core.category.infrastructure.django_app.models import Category as CategoryModel
from core._shared.listing.orderer import Order
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestGetAll:
    @pytest.fixture
    def repository(self):
        return CategoryDjangoRepository()

    @pytest.fixture
    def categories(self):
        # Create 5 sample categories in the database
        return CategoryModel.objects.bulk_create(
            [CategoryModel(name=f"Category {i}", description=f"Description for Category {i}") for i in range(5)]
        )

    def test_no_parameters_returns_all_categories(self, repository, categories):
        result = repository.get_all()
        assert len(result) == 5

    def test_limit_parameter_limits_returned_categories(self, repository, categories):
        result = repository.get_all(limit=2)
        assert len(result) == 2

    def test_offset_parameter_skips_categories(self, repository, categories):
        result = repository.get_all(offset=3)
        assert len(result) == 2

    def test_order_by_ascending(self, repository, categories):
        result = repository.get_all(order_by={"name": Order.ASC})
        assert result[0].name == "Category 0"
        assert result[1].name == "Category 1"

    def test_order_by_descending(self, repository, categories):
        result = repository.get_all(order_by={"name": Order.DESC})
        assert result[0].name == "Category 4"
        assert result[1].name == "Category 3"

    def test_filters(self, repository, categories):
        result = repository.get_all(filters={"name": "Category 2"})
        assert len(result) == 1
        assert result[0].name == "Category 2"
