import logging
from typing import Optional
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.category.domain.entity.category_interface import CategoryInterface


class Category(CategoryInterface, AbstractEntity):
    def __init__(
        self,
        *,
        name: str,
        description: str = "",
        is_active: bool = True,
        id: Optional[UUID] = None,
    ) -> None:
        super().__init__()
        if not id:
            id = uuid4()

        self.__id = id
        self.__name = name
        self.__description = description
        self.__is_active = is_active

        super().__init__()
        self._validate()
        if self.notification.has_errors():
            raise NotificationException(self.notification.errors)

    def __repr__(self):
        return f"<Category {self.name}>"

    def __eq__(self, other: "Category") -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def _validate(self) -> None:  # TODO: decouple validation from Entity with a Validator
        if not self.name:
            self.notification.add_error(NotificationError(message="Category name cannot be empty", context="category"))
        if len(self.name) > 255:
            self.notification.add_error(
                NotificationError(message="Category name cannot be longer than 255 characters", context="category")
            )
        if len(self.description) > 1024:
            self.notification.add_error(
                NotificationError(
                    message="Category description cannot be longer than 1024 characters",
                    context="category",
                )
            )

    def activate(self) -> None:
        logging.info(f"Activating category {self.name}")
        self.__is_active = True
        self._validate()

    def deactivate(self) -> None:
        logging.info(f"Activating category {self.name}")
        self.__is_active = False
        self._validate()

    def change_category(self, name: str, description: str) -> None:
        logging.info(f"Changing category {self.name} to {name} wih description {description}")
        self.__name = name
        self.__description = description
        self._validate()

    def activate(self) -> None:
        self.__is_active = True
        self._validate()

    def deacivate(self) -> None:
        self.__is_active = False
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
    def id(self) -> UUID:
        return self.__id
