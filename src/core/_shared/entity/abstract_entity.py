from abc import ABC
from dataclasses import dataclass, field
from typing import List, Dict, Any

from pydantic import TypeAdapter, ValidationError

from core._shared.events.event import DomainEvent
from core._shared.events.event_service import EventServiceInterface
from core._shared.notification.notification import Notification
from core._shared.notification.notification_error import NotificationError


@dataclass(slots=True)
class AbstractEntity(ABC):
    notification: Notification = field(init=False, default_factory=Notification)
    events: List[DomainEvent] = field(init=False, default_factory=list)

    def add_event(self, event: DomainEvent) -> None:
        self.events.append(event)

    def dispatch_events(self, event_service: EventServiceInterface) -> None:
        for event in self.events:
            event_service.send(event)

        self.events = []

    def _validate(self, data: Dict[str, Any]):
        try:
            TypeAdapter(self.__class__).validate_python(data)
        except ValidationError as e:
            for error in e.errors():
                self.notification.add_error(NotificationError(message=error["msg"], context=error["loc"][0]))
