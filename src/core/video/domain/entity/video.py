from dataclasses import dataclass, asdict, field
from decimal import Decimal
from typing import Set
from uuid import UUID, uuid4

from core._shared.entity.abstract_entity import AbstractEntity
from core.video.domain.events import AudioVideoMediaUpdated
from core.video.domain.entity.value_objects import (
    Rating,
    ImageMedia,
    AudioVideoMedia,
)


@dataclass(slots=True)
class Video(AbstractEntity):
    title: str
    description: str
    launch_year: int
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

    id: UUID = field(default_factory=uuid4)

    def add_categories(self, categories: Set[UUID]):
        self.categories.update(categories)
        self.validate()  # TODO: do I have to call validate after every mutation?

    def add_genres(self, genres: Set[UUID]):
        self.genres.update(genres)
        self.validate()

    def add_cast_members(self, cast_members: Set[UUID]):
        self.cast_members.update(cast_members)
        self.validate()

    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        opened: bool,
        published: bool,
        rating: Rating,
        categories: Set[UUID],
        genres: Set[UUID],
        cast_members: Set[UUID],
    ) -> "Video":
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.opened = opened
        self.published = published
        self.rating = rating
        self.categories = categories
        self.genres = genres
        self.cast_members = cast_members
        self.validate()
        return self

    def validate(self):
        self._validate(asdict(self))

    def update_banner(self, banner: ImageMedia):
        self.banner = banner
        return self

    def update_thumbnail(self, thumbnail: ImageMedia):
        self.thumbnail = thumbnail
        return self

    def update_thumbnail_half(self, thumbnail_half: ImageMedia):
        self.thumbnail_half = thumbnail_half
        return self

    def update_video(self, video: AudioVideoMedia):
        self.video = video
        self.add_event(AudioVideoMediaUpdated({"video_id": self.id, "media_id": video.id, "type": "video"}))
        return self

    def update_trailer(self, trailer: AudioVideoMedia):
        self.trailer = trailer
        self.add_event(AudioVideoMediaUpdated({"video_id": self.id, "media_id": trailer.id, "type": "trailer"}))
        return self
