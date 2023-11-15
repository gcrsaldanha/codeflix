from abc import ABC, abstractmethod

from core._shared.events.event import DomainEvent


class IEventHandler(ABC):
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        raise NotImplementedError
