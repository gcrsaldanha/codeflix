from dataclasses import dataclass

from core._shared.events.event import Event


@dataclass(frozen=True, slots=True)
class TrailerUpdated(Event):
    pass


@dataclass(frozen=True, slots=True)
class TrailerUploaded(Event):
    pass


@dataclass(frozen=True, slots=True)
class VideoUpdated(Event):
    pass


@dataclass(frozen=True, slots=True)
class VideoUploaded(Event):
    pass
