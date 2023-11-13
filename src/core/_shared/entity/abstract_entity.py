from abc import ABC
from dataclasses import dataclass, field

from core._shared.events.event_dispatcher import EventDispatcher
from core._shared.notification.notification import Notification
from core._shared.notification.notification_interface import NotificationInterface


@dataclass(slots=True)
class AbstractEntity(ABC):
    notification: Notification = field(init=False)
    dispatcher: EventDispatcher = field(init=False)

    def __post_init__(self):
        self.notification: NotificationInterface = Notification()
        self.dispatcher: EventDispatcher = EventDispatcher()
