import logging
from dataclasses import dataclass, field, asdict
from typing import Optional
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.category.domain.entity.category_interface import CategoryInterface


@dataclass(eq=False)
class Category(CategoryInterface, AbstractEntity):
    name: str
    id: Optional[UUID] = field(default_factory=uuid4)
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()
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

    def validate(self) -> None:
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
        self.validate()

    def deactivate(self) -> None:
        logging.info(f"Activating category {self.name}")
        self.is_active = False
        self.validate()

    def change_category(self, name: str, description: str) -> None:
        logging.info(f"Changing category {self.name} to {name} wih description {description}")
        self.name = name
        self.description = description
        self.validate()
