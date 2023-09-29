from typing import Iterable, List

from domain._shared.notification.notification_error import NotificationError
from domain._shared.notification.notification_interface import NotificationInterface


class Notification(NotificationInterface):
    def __init__(self) -> None:
        self._errors: List[NotificationError] = []

    def add_error(self, error: NotificationError) -> None:
        self._errors.append(error)

    def messages(self, context: str) -> str:
        filter_by_context = filter(lambda message: message.context == context if context else True, self._errors)

        return ",".join([str(error) for error in filter_by_context])

    @property
    def errors(self) -> Iterable[NotificationError]:
        yield from self._errors

    def has_errors(self) -> bool:
        return bool(self._errors)
