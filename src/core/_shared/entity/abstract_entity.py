from abc import ABC

from core._shared.notification.notification import Notification
from core._shared.notification.notification_interface import NotificationInterface


class AbstractEntity(ABC):
    def __init__(self) -> None:
        self.notification: NotificationInterface = Notification()
