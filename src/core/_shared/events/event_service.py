from abc import ABC

from core._shared.events.event import DomainEvent


class EventServiceInterface(ABC):
    def send(self, event: DomainEvent) -> None:
        raise NotImplementedError


class EventService(EventServiceInterface):
    def send(self, event: DomainEvent) -> None:
        print("Sending event", event)
