from dataclasses import dataclass

from core._shared.events.event import DomainEvent


@dataclass(frozen=True, slots=True)
class AudioVideoMediaUpdated(DomainEvent):
    pass
