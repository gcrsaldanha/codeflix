from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Set
from uuid import UUID

from core._shared.application.use_case import UseCase
from core._shared.notification.notification import Notification
from core._shared.notification.notification_error import NotificationError, NotificationException
from core.cast_member.domain.repository.cast_member_repository_interface import CastMemberRepositoryInterface
from core.cast_member.infrastructure.cast_member_app.repositories import CastMemberDjangoRepository
from core.category.domain.repository.category_repository_interface import CategoryRepositoryInterface
from core.category.infrastructure.django_app.repositories import CategoryDjangoRepository
from core.genre.infrastructure.genre_django_app.repositories import (
    GenreRepositoryInterface,
    GenreDjangoRepository,
)
from core.video.domain.entity.video import Video
from core.video.domain.storage_service_interface import StorageServiceInterface
from core.video.domain.entity.value_objects import Resource, MediaResource, MediaType
from core.video.domain.entity.value_objects import Rating
from core.video.domain.video_repository_interface import VideoRepositoryInterface
from core.video.infrastructure.services.gcp_storage_service import GCPStorageService
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
    banner: Resource | None = None
    thumbnail: Resource | None = None
    thumbnail_half: Resource | None = None
    trailer: Resource | None = None
    video: Resource | None = None


"""
- Only video needs encoding
- If video is passed, all other "medias" must be provided
- Other medias can be updated
"""


@dataclass
class CreateVideoOutput:
    id: UUID


class CreateVideoUseCase(UseCase[CreateVideoInput, CreateVideoOutput]):
    def __init__(
        self,
        video_repository: Optional[VideoRepositoryInterface] = None,
        category_repository: Optional[CategoryRepositoryInterface] = None,
        genre_repository: Optional[GenreRepositoryInterface] = None,
        cast_member_repository: Optional[CastMemberRepositoryInterface] = None,
        storage_service: Optional[StorageServiceInterface] = None,
    ):
        # TODO: Too many repositories? Do I need to check if all entities exist?
        self._video_repository = video_repository or VideoDjangoRepository()
        self._category_repository = category_repository or CategoryDjangoRepository()
        self._genre_repository = genre_repository or GenreDjangoRepository()
        self._cast_member_repository = cast_member_repository or CastMemberDjangoRepository()
        self._storage_service = storage_service or GCPStorageService("mock", "mock")

    def execute(self, request: CreateVideoInput) -> CreateVideoOutput:
        # TODO: these validations can be grouped into a central validator for the usecase
        notification = Notification()
        notification.add_error(self.validate_categories(request.categories))
        notification.add_error(self.validate_genres(request.genres))
        notification.add_error(self.validate_cast_members(request.cast_members))

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
        )

        entity.validate()
        if entity.notification.has_errors():
            # TODO: expose notification.add_errors(errors: List[NotificationError])
            for error in entity.notification.errors:
                notification.add_error(error)
            raise NotificationException(entity.notification.errors)

        # TODO: add if conditions to only store if is not null
        # For simplicity now, assuming all values are provided
        video = self._storage_service.store_video(
            MediaResource(resource=request.video, type=MediaType.VIDEO),
            entity.id,
        )
        trailer = self._storage_service.store_video(
            MediaResource(resource=request.trailer, type=MediaType.TRAILER),
            entity.id,
        )
        banner = self._storage_service.store_image(
            MediaResource(resource=request.banner, type=MediaType.BANNER),
            entity.id,
        )
        thumbnail = self._storage_service.store_image(
            MediaResource(resource=request.thumbnail, type=MediaType.THUMBNAIL),
            entity.id,
        )
        thumbnail_half = self._storage_service.store_image(
            MediaResource(resource=request.thumbnail_half, type=MediaType.THUMBNAIL_HALF),
            entity.id,
        )

        self._video_repository.create(
            entity.update_video(video)
            .update_trailer(trailer)
            .update_banner(banner)
            .update_thumbnail(thumbnail)
            .update_thumbnail_half(thumbnail_half)
        )

        return CreateVideoOutput(id=entity.id)

    def validate_categories(self, category_ids: Set[UUID]) -> NotificationError:
        categories = self._category_repository.get_all(filters={"id__in": category_ids})
        if len(categories) != len(category_ids):
            return NotificationError(message="Invalid categories", context="categories")

    def validate_genres(self, genre_ids: Set[UUID]) -> NotificationError:
        genres = self._genre_repository.get_all(filters={"id__in": genre_ids})
        if len(genres) != len(genre_ids):
            return NotificationError(message="Invalid genres", context="genres")

    def validate_cast_members(self, cast_member_ids: Set[UUID]) -> NotificationError:
        cast_members = self._cast_member_repository.get_all(filters={"id__in": cast_member_ids})
        if len(cast_members) != len(cast_member_ids):
            return NotificationError(message="Invalid cast members", context="cast_members")
