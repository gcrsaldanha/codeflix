import logging
from typing import Optional, Set, TypeVar, NewType
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.genre.domain.entity.genre_interface import GenreInterface


class Genre(GenreInterface, AbstractEntity):
    def __init__(
        self,
        *,
        name: str,
        description: str = "",
        is_active: bool = True,
        id: Optional[UUID] = None,
        categories: Optional[Set[UUID]] = None,
    ) -> None:
        super().__init__()
        if not id:
            id = uuid4()

        self.__id = id
        self.__name = name
        self.__description = description
        self.__is_active = is_active
        self.__categories = set(categories or [])

        super().__init__()
        self._validate()
        if self.notification.has_errors():
            raise NotificationException(self.notification.errors)

    def __repr__(self):
        return f"<Genre {self.name}>"

    def __eq__(self, other: "Genre") -> bool:
        if not isinstance(other, Genre):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _validate(self) -> None:  # TODO: decouple validation from Entity with a Validator
        if not self.name:
            self.notification.add_error(NotificationError(message="Genre name cannot be empty", context="genre"))
        if len(self.name) > 255:
            self.notification.add_error(
                NotificationError(message="Genre name cannot be longer than 255 characters", context="genre")
            )
        if len(self.description) > 1024:
            self.notification.add_error(
                NotificationError(
                    message="Genre description cannot be longer than 1024 characters",
                    context="genre",
                )
            )

    def activate(self) -> None:
        logging.info(f"Activating genre {self.name}")
        self.__is_active = True
        self._validate()

    def deactivate(self) -> None:
        logging.info(f"Activating genre {self.name}")
        self.__is_active = False
        self._validate()

    def change_genre(self, name: str, description: str) -> None:
        logging.info(f"Changing genre {self.name} to {name} wih description {description}")
        self.__name = name
        self.__description = description
        self._validate()

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def categories(self) -> Set[UUID]:
        return self.__categories

    def add_category(self, category: UUID) -> None:  # TODO: add categories
        if category not in self.__categories:
            self.__categories.add(category)
        self._validate()

    def remove_category(self, category: UUID) -> None:
        if category in self.__categories:
            self.__categories.remove(category)
        self._validate()

    @property
    def id(self) -> UUID:
        return self.__id
