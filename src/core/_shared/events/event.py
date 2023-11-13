from abc import ABC
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict


@dataclass(slots=True, frozen=True)
class Event(ABC):
    payload: Dict = field(default_factory=dict)

    @property
    def type(self) -> str:
        return self.__class__.__name__
