import enum
from dataclasses import dataclass
from enum import Enum, auto, unique
from uuid import UUID


@unique
class Rating(Enum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()


@unique
class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()


@dataclass(frozen=True, eq=True, slots=True)
class ImageMedia:
    id: UUID | str
    checksum: str
    name: str
    location: str


@dataclass(frozen=True, eq=True, slots=True)
class AudioVideoMedia:
    id: UUID | str
    checksum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus


@dataclass(frozen=True, slots=True)
class Resource:
    content: bytes
    checksum: str
    content_type: str
    name: str


@enum.unique
class MediaType(Enum):
    VIDEO = auto()
    TRAILER = auto()
    BANNER = auto()
    THUMBNAIL = auto()
    THUMBNAIL_HALF = auto()


@dataclass(frozen=True, slots=True)
class MediaResource:
    resource: Resource
    type: MediaType
