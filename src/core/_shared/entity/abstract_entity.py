from abc import ABC
from dataclasses import dataclass, field
from typing import List

from core._shared.events.event import DomainEvent
from core._shared.notification.notification import Notification
from core._shared.notification.notification_interface import NotificationInterface


class EventServiceInterface(ABC):  # TODO: move to another module
    def send(self, event: DomainEvent) -> None:
        raise NotImplementedError


class EventService(EventServiceInterface):  # TODO: move to another module
    def send(self, event: DomainEvent) -> None:
        print("Sending event", event)


@dataclass(slots=True)
class AbstractEntity(ABC):
    notification: Notification = field(init=False)
    events: List[DomainEvent] = field(init=False)

    def __post_init__(self):
        self.notification: NotificationInterface = Notification()
        self.events: List[DomainEvent] = []

    def add_event(self, event: DomainEvent) -> None:
        self.events.append(event)

    def dispatch_events(self, event_service: EventServiceInterface) -> None:
        for event in self.events:
            event_service.send(event)

        self.events = []
