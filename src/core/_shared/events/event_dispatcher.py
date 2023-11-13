from abc import ABC, abstractmethod
from typing import Dict, List

from core._shared.events.event_handler import IEventHandler


class IEventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event) -> None:
        raise NotImplementedError

    @abstractmethod
    def register(self, event_type: str, handler: IEventHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister(self, event_type: str, handler: IEventHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister_all(self) -> None:
        raise NotImplementedError


class EventDispatcher(IEventDispatcher):
    def __init__(self):
        self._handlers: Dict[str, List[IEventHandler]] = {}

    def dispatch(self, event) -> None:
        event_type = event.type

        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler.handle(event)

    def register(self, event_type: str, handler: IEventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)

    def unregister(self, event_type: str, handler: IEventHandler) -> None:
        if event_type in self._handlers:
            self._handlers[event_type].remove(handler)

    def unregister_all(self) -> None:
        self._handlers = {}
