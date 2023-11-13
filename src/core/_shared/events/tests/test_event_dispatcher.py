from dataclasses import dataclass
from unittest.mock import create_autospec
from core._shared.events.event import Event
from core._shared.events.event_dispatcher import EventDispatcher
from core._shared.events.event_handler import IEventHandler


class FakeHandler(IEventHandler):
    def handle(self, event: Event) -> None:
        print(f"Handling event: {event.__class__.__name__} with payload: {event.payload}")


@dataclass(frozen=True, slots=True)
class FakeEventCreated(Event):
    pass


def test_should_register_an_event_handler():
    event_dispatcher = EventDispatcher()
    handler = FakeHandler()
    event = FakeEventCreated()
    event_type = event.__class__.__name__

    event_dispatcher.register(event_type=event_type, handler=handler)

    assert event_dispatcher._handlers[event_type] == [handler]


def test_should_unregister_an_event_handler():
    event_dispatcher = EventDispatcher()
    handler = FakeHandler()
    event = FakeEventCreated(payload={"custom_attribute": "abc"})
    event_type = event.__class__.__name__
    event_dispatcher.register(event_type=event_type, handler=handler)

    event_dispatcher.unregister(event_type=event_type, handler=handler)

    assert event_dispatcher._handlers[event_type] == []


def test_should_dispatch_event_to_handler():
    event_dispatcher = EventDispatcher()
    handler = create_autospec(IEventHandler)
    event = FakeEventCreated({"custom_attribute": "abc"})
    event_type = event.__class__.__name__
    event_dispatcher.register(event_type=event_type, handler=handler)

    event_dispatcher.dispatch(event)

    assert event_dispatcher._handlers[event_type] == [handler]
    handler.handle.assert_called_once_with(event)
