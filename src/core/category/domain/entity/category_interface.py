from abc import ABC, abstractmethod


class CategoryInterface(ABC):
    @abstractmethod
    def activate(self) -> None:
        pass

    @abstractmethod
    def deactivate(self) -> None:
        pass

    @abstractmethod
    def change_category(self, name: str, description: str) -> None:
        pass
