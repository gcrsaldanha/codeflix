import logging
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.category.domain.entity.category_interface import CategoryInterface


@dataclass(eq=False)
class Category(CategoryInterface, AbstractEntity):
    name: str
    id: Optional[UUID] = None
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        super().__init__()

        if not self.id:
            self.id = uuid4()

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
        self.is_active = True
        self._validate()

    def deactivate(self) -> None:
        logging.info(f"Activating category {self.name}")
        self.is_active = False
        self._validate()

    def change_category(self, name: str, description: str) -> None:
        logging.info(f"Changing category {self.name} to {name} wih description {description}")
        self.name = name
        self.description = description
        self._validate()
