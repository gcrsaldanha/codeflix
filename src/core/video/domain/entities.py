from dataclasses import dataclass, asdict
from decimal import Decimal
from typing import Set
from uuid import UUID

from pydantic import TypeAdapter
from pydantic_core import ValidationError

from core._shared.entity.abstract_entity import AbstractEntity
from core._shared.notification.notification_error import NotificationException, NotificationError
from core.video.domain.value_objects import (
    Rating,
    ImageMedia,
    AudioVideoMedia,
)


@dataclass(slots=True)
class Video(AbstractEntity):
    title: str
    description: str
    launch_year: int  # changed from launched_at to  launch_year
    duration: Decimal
    opened: bool
    published: bool
    rating: Rating

    categories: Set[UUID]
    genres: Set[UUID]
    cast_members: Set[UUID]

    # Optional
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    # def __post_init__(self):
    #     self.validate()
    #     if self.notification.has_errors():
    #         raise NotificationException(self.notification.errors)

    def validate(self):
        try:
            TypeAdapter(self.__class__).validate_python(asdict(self))
        except ValidationError as e:
            for error in e.errors():
                self.notification.add_error(NotificationError(message=error["msg"], context=error["loc"][0]))


"""
{'type': 'string_type', 'loc': ('name',), 'msg': 'Input should be a valid string', 'input': 10, 'url': 'https://errors.pydantic.dev/2.4/v/string_type'}
{'type': 'uuid_parsing', 'loc': ('id',), 'msg': 'Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1', 'input': 'iddasdfaf', 'ctx': {'error': 'invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1'}, 'url': 'https://errors.pydantic.dev/2.4/v/uuid_parsing'}
"""
