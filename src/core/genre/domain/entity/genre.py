import logging
from dataclasses import dataclass, field
from typing import Optional, Set
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.genre.domain.entity.genre_interface import GenreInterface


@dataclass(slots=True, kw_only=True)
class Genre(GenreInterface, AbstractEntity):
    name: str
    id: Optional[UUID] = field(default_factory=uuid4)
    description: str = ""
    is_active: bool = True
    categories: Set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()
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

    def validate(self) -> None:
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
        self.is_active = True
        self.validate()

    def deactivate(self) -> None:
        logging.info(f"Activating genre {self.name}")
        self.is_active = False
        self.validate()

    def change_genre(self, name: str, description: str) -> None:
        logging.info(f"Changing genre {self.name} to {name} wih description {description}")
        self.name = name
        self.description = description
        self.validate()

    def add_categories(self, categories: Set[UUID]) -> None:
        self.categories = self.categories | categories
        self.validate()

    def add_category(self, category: UUID) -> None:
        self.add_categories({category})
        self.validate()
    def remove_category(self, category: UUID) -> None:
        if category in self.categories:
            self.categories.remove(category)
        self.validate()
