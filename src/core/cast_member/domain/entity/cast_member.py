import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.cast_member.domain.entity.cast_member_interface import CastMemberInterface


class CastMemberType(Enum):
    DIRECTOR = "director"
    ACTOR = "actor"


@dataclass(slots=True, kw_only=True)
class CastMember(CastMemberInterface, AbstractEntity):
    name: str
    cast_member_type: CastMemberType
    id: Optional[UUID] = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()
        if self.notification.has_errors():
            raise NotificationException(self.notification.errors)

    def __repr__(self):
        return f"<CastMember {self.name}, Type: {self.cast_member_type}>"

    def __eq__(self, other: "CastMember") -> bool:
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def validate(self) -> None:
        if not self.name:
            self.notification.add_error(NotificationError(message="name cannot be empty", context="cast_member"))
        if len(self.name) > 255:
            self.notification.add_error(
                NotificationError(message="name cannot be longer than 255 characters", context="cast_member")
            )
        if not self.cast_member_type:
            self.notification.add_error(NotificationError(message="type cannot be empty", context="cast_member"))

    def change_cast_member(self, name: str, cast_member_type: CastMemberType) -> None:
        logging.info(f"Changing CastMember {self.name} to {name} wih type {cast_member_type}")
        self.name = name
        self.cast_member_type = cast_member_type
        self.validate()
