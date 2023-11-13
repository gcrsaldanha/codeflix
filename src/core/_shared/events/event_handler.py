from abc import ABC, abstractmethod

from core._shared.events.event import Event


class IEventHandler(ABC):

    @abstractmethod
    def handle(self, event: Event) -> None:
        raise NotImplementedError
