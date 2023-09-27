import logging
from typing import Optional
from uuid import UUID, uuid4

from category_interface import CategoryInterface


class Category(CategoryInterface):
    def __init__(
        self,
        *,
        name: str,
        description: str = "",
        is_active: bool = True,
        id: Optional[UUID] = None,
    ) -> None:
        if not id:
            id = uuid4()

        self.__id = id
        self.__name = name
        self.__description = description
        self.__is_active = is_active

        self.validate()

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

    def validate(self) -> None:
        if not self.name:
            raise ValueError("Category name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("Category name cannot be longer than 255 characters")

    def activate(self) -> None:
        logging.info(f"Activating category {self.name}")
        self.__is_active = True
        self.validate()

    def deactivate(self) -> None:
        logging.info(f"Activating category {self.name}")
        self.__is_active = False
        self.validate()

    def change_category(self, name: str, description: str) -> None:
        logging.info(f"Changing category {self.name} to {name} wih description {description}")
        self.__name = name
        self.__description = description
        self.validate()
