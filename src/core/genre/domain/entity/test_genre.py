from uuid import UUID, uuid4

import pytest

from core._shared.notification.notification_error import NotificationException
from core.category.domain import Category
from core.genre.domain.entity.genre import Genre


# TODO: Make these tests more realistic (genre names vs categories)
class TestGenreInit:
    def test_create_genre_with_auto_id(self):
        genre = Genre(name="Drama", description="Genre for drama")
        assert genre.name == "Drama"
        assert genre.description == "Genre for drama"
        assert genre.is_active is True
        assert genre.categories == []
        assert genre.id is not None
        assert isinstance(genre.id, UUID)

    def test_create_genre_with_given_id(self):
        given_genre_id = uuid4()
        genre = Genre(name="Drama", description="Genre for drama", id=given_genre_id)
        assert genre.name == "Drama"
        assert genre.description == "Genre for drama"
        assert genre.is_active is True
        assert genre.categories == []
        assert genre.id == given_genre_id

    def test_create_genre_with_list_of_categories(self):
        category_1 = Category(name="Category 1", description="Category 1 description")
        category_2 = Category(name="Category 2", description="Category 2 description")
        genre = Genre(name="Drama", description="Genre for drama", categories=[category_1, category_2])
        assert genre.name == "Drama"
        assert genre.description == "Genre for drama"
        assert genre.is_active is True
        assert genre.categories == [category_1, category_2]
        assert genre.id is not None
        assert isinstance(genre.id, UUID)

    def test_when_genre_is_created_with_duplicate_categories_then_dedupe_them(self):
        category = Category(name="Drama", description="Category for drama")
        genre = Genre(name="Genre Name", description="Any Genre", categories=[category, category])
        assert genre.categories == [category]

    def test_when_name_is_empty_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="Genre name cannot be empty"):
            Genre(name="")

    def test_when_is_larger_than_255_characters_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="Genre name cannot be longer than 255 characters"):
            Genre(name="a" * 256)

    def test_when_description_is_larger_than_1024_characters_then_raise_notification_error(self):
        with pytest.raises(NotificationException, match="Genre description cannot be longer than 1024 characters"):
            Genre(name="Drama", description="a" * 1025)

    def test_when_multiple_errors_then_raise_multiple_notification_error(self):
        expected_notification_message = "genre: Genre name cannot be empty,genre: Genre description cannot be longer than 1024 characters"  # noqa: E501
        with pytest.raises(NotificationException, match=expected_notification_message):
            Genre(name="", description="a" * 1025)


class TestActivate:
    @pytest.mark.parametrize("is_active", [True, False])
    def test_when_genre_is_inactive_then_activate_it(self, is_active):
        genre = Genre(name="Drama", description="Genre for drama", is_active=False)
        genre.activate()
        assert genre.is_active is True

    def test_when_genre_is_active_then_do_nothing(self):
        genre = Genre(name="Drama", description="Genre for drama", is_active=True)
        genre.activate()
        assert genre.is_active is True


class TestDeactivate:
    def test_when_genre_is_active_then_deactivate_it(self):
        genre = Genre(name="Drama", description="Genre for drama", is_active=True)
        genre.deactivate()
        assert genre.is_active is False

    def test_when_genre_is_inactive_then_do_nothing(self):
        genre = Genre(name="Drama", description="Genre for drama", is_active=False)
        genre.deactivate()
        assert genre.is_active is False


class TestChangeGenre:
    def test_change_genre_name_and_description(self):
        genre = Genre(name="Drama", description="Genre for drama")
        genre.change_genre(name="Comedy", description="Genre for comedy")
        assert genre.name == "Comedy"
        assert genre.description == "Genre for comedy"

    def test_when_name_is_empty_then_add_notification_error(self):
        genre = Genre(name="Drama", description="Genre for drama")
        genre.change_genre(name="", description="Genre for drama")
        assert genre.notification.has_errors()
        assert genre.notification.messages() == "genre: Genre name cannot be empty"


class TestAddCategory:
    def test_add_category(self):
        category = Category(name="Category 1", description="Category 1 description")
        genre = Genre(name="Drama", description="Genre for drama")
        genre.add_category(category)
        assert genre.categories == [category]

    def test_when_category_already_exists_then_do_nothing(self):
        category = Category(name="Category 1", description="Category 1 description")
        genre = Genre(name="Drama", description="Genre for drama", categories=[category])
        genre.add_category(category)
        assert genre.categories == [category]


class TestRemoveCategory:
    def test_remove_category(self):
        category = Category(name="Category 1", description="Category 1 description")
        category_2 = Category(name="Category 2", description="Category 2 description")
        genre = Genre(name="Drama", description="Genre for drama", categories=[category, category_2])
        genre.remove_category(category)
        assert genre.categories == [category_2]

    def test_when_category_does_not_exist_then_do_nothing(self):
        category = Category(name="Category 1", description="Category 1 description")
        genre = Genre(name="Drama", description="Genre for drama")
        genre.remove_category(category)
        assert genre.categories == []
