from uuid import UUID, uuid4
import pytest

from domain.category.entity.category import Category


class TestCategoryInit:
    def test_create_category_with_auto_id(self):
        category = Category(name="Drama", description="Category for drama")
        assert category.name == "Drama"
        assert category.description == "Category for drama"
        assert category.is_active is True
        assert category.id is not None
        assert isinstance(category.id, UUID)

    def test_create_category_with_given_id(self):
        given_category_id = uuid4()
        category = Category(name="Drama", description="Category for drama", id=given_category_id)
        assert category.name == "Drama"
        assert category.description == "Category for drama"
        assert category.is_active is True
        assert category.id == given_category_id

    def test_when_name_is_empty_then_raise_value_error(self):
        try:
            Category(name="")
            assert False
        except ValueError:
            assert True


class TestValidate:
    def test_when_name_is_empty_then_raise_value_error(self):
        # The only way to create a category with a "bad name" directly is if I access the private variable.
        category = Category(name="Drama")
        with pytest.raises(ValueError, match="Category name cannot be empty"):
            category.change_category(name="", description="Category for drama")

    def test_when_name_is_longer_than_255_characters_then_raise_value_error(self):
        category = Category(name="Drama")
        with pytest.raises(ValueError, match="Category name cannot be longer than 255 characters"):
            category.change_category(name="a" * 256, description="Category for drama")


class TestActivate:
    def test_when_category_is_inactive_then_activate_it(self):
        category = Category(name="Drama", description="Category for drama", is_active=False)
        category.activate()
        assert category.is_active is True

    def test_when_category_is_active_then_do_nothing(self):
        category = Category(name="Drama", description="Category for drama", is_active=True)
        category.activate()
        assert category.is_active is True


class TestDeactivate:
    def test_when_category_is_active_then_deactivate_it(self):
        category = Category(name="Drama", description="Category for drama", is_active=True)
        category.deactivate()
        assert category.is_active is False

    def test_when_category_is_inactive_then_do_nothing(self):
        category = Category(name="Drama", description="Category for drama", is_active=False)
        category.deactivate()
        assert category.is_active is False


class TestChangeCategory:
    def test_change_category_name_and_description(self):
        category = Category(name="Drama", description="Category for drama")
        category.change_category(name="Comedy", description="Category for comedy")
        assert category.name == "Comedy"
        assert category.description == "Category for comedy"

    def test_when_name_is_empty_then_raise_value_error(self):
        category = Category(name="Drama", description="Category for drama")
        with pytest.raises(ValueError, match="Category name cannot be empty"):
            category.change_category(name="", description="Category for drama")
