from abc import ABC, abstractmethod
from typing import Iterable

from core._shared.notification.notification_error import NotificationError


class NotificationInterface(ABC):
    @abstractmethod
    def add_error(self, error: NotificationError) -> None:
        pass

    @abstractmethod
    def messages(self, context: str = "") -> str:
        pass

    @property
    @abstractmethod
    def errors(self) -> Iterable[NotificationError]:
        pass

    @abstractmethod
    def has_errors(self) -> bool:
        pass
