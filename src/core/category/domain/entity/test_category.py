from uuid import UUID, uuid4
import pytest

from core._shared.notification.notification_error import NotificationException
from core.category.domain.entity.category import Category


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

    def test_when_name_is_empty_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="Category name cannot be empty"):
            Category(name="")

    def test_when_is_larger_than_255_characters_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="Category name cannot be longer than 255 characters"):
            Category(name="a" * 256)

    def test_when_description_is_larger_than_1024_characters_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="Category description cannot be longer than 1024 characters"):
            Category(name="Drama", description="a" * 1025)

    def test_when_multiple_errors_then_raise_multiple_notification_error(self):
        expected_notification_message = "category: Category name cannot be empty,category: Category description cannot be longer than 1024 characters"  # noqa: E501
        with pytest.raises(NotificationException, match=expected_notification_message):
            Category(name="", description="a" * 1025)


class TestActivate:
    @pytest.mark.parametrize("is_active", [True, False])
    def test_when_category_is_inactive_then_activate_it(self, is_active):
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

    def test_when_name_is_empty_then_add_notification_error(self):
        category = Category(name="Drama", description="Category for drama")
        category.change_category(name="", description="Category for drama")
        assert category.notification.has_errors()
        assert category.notification.messages() == "category: Category name cannot be empty"
