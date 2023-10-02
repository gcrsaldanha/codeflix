from abc import ABC

from domain._shared.notification.notification import Notification
from domain._shared.notification.notification_interface import NotificationInterface


class AbstractEntity(ABC):
    def __init__(self) -> None:
        self.notification: NotificationInterface = Notification()
