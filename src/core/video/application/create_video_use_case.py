from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Set
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberDjangoRepository
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.genre.infrastructure.genre_django_app.repositories import (
    GenreRepositoryInterface,
    GenreDjangoRepository,
)
from core.video.domain.entities import Video
from core.video.domain.value_objects import ImageMedia
from core.video.domain.value_objects import Rating, AudioVideoMedia
from core.video.domain.video_repository import VideoRepositoryInterface
from core.video.infrastructure.video_django_app.repositories import VideoDjangoRepository


@dataclass
class CreateVideoInput:
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
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None


@dataclass
class CreateVideoOutput:
    id: UUID


class CreateVideoUseCase(UseCase[CreateVideoInput, CreateVideoOutput]):
    def __init__(
        self,
        repository: Optional[VideoRepositoryInterface] = None,
        category_repository: Optional[CategoryRepositoryInterface] = None,
        genre_repository: Optional[GenreRepositoryInterface] = None,
        cast_member_repository: Optional[CastMemberRepositoryInterface] = None,
    ):
        # TODO: Too many repositories? Do I need to check if all entities exist?
        self._repository = repository or VideoDjangoRepository()
        self._category_repository = category_repository or CategoryDjangoRepository()
        self._genre_repository = genre_repository or GenreDjangoRepository()
        self._cast_member_repository = cast_member_repository or CastMemberDjangoRepository()

    def execute(self, request: CreateVideoInput) -> CreateVideoOutput:
        """
        - fetch/validate all related entities: genre, category, cast_member?
        - validate genres/categories are related?
        - create video with media or not (optional values)
        - persist video
        """
        entity = Video(
            title=request.title,
            description=request.description,
            launch_year=request.launch_year,
            duration=request.duration,
            opened=request.opened,
            published=request.published,
            rating=request.rating,
            categories=request.categories,
            genres=request.genres,
            cast_members=request.cast_members,
            banner=request.banner,
            thumbnail=request.thumbnail,
            thumbnail_half=request.thumbnail_half,
            trailer=request.trailer,
            video=request.video,
        )

        entity.validate()  # Does this need to be called?
        if entity.notification.has_errors():
            raise ValueError(entity.notification.errors)

        self._repository.create(entity)

        return CreateVideoOutput(id=entity.id)
