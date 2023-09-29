from typing import Iterable


class NotificationError:
    def __init__(self, message: str, context: str) -> None:
        self.message = message
        self.context = context

    def __str__(self) -> str:
        return f"{self.context}: {self.message}"


class NotificationException(Exception):
    def __init__(self, errors: Iterable[NotificationError]) -> None:
        self.errors = errors
        super().__init__(",".join([str(error) for error in errors]))
