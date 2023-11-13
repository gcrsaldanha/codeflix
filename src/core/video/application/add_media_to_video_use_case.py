from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from core._shared.application.use_case import UseCase
from core.video.domain.value_objects import AudioVideoMedia
from core.video.domain.value_objects import ImageMedia
from core.video.domain.video_repository import VideoRepositoryInterface
from core.video.infrastructure.video_django_app.repositories import VideoDjangoRepository


@dataclass
class AddMediaToVideoInput:
    id: UUID
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None


@dataclass
class AddMediaToVideoOutput:
    id: UUID


class AddMediaToVideoUseCase(UseCase[AddMediaToVideoInput, AddMediaToVideoOutput]):
    def __init__(
        self,
        repository: Optional[VideoRepositoryInterface] = None,
    ):
        self._repository = repository or VideoDjangoRepository()

    def execute(self, request: AddMediaToVideoInput) -> AddMediaToVideoOutput:
        entity = self._repository.get_by_id(request.id)

        if request.banner:
            entity.update_banner(request.banner)
        if request.thumbnail:
            entity.update_thumbnail(request.thumbnail)
        if request.thumbnail_half:
            entity.update_thumbnail_half(request.thumbnail_half)
        if request.trailer:
            entity.update_trailer(request.trailer)
        if request.video:
            entity.update_video(request.video)

        entity.validate()
        if entity.notification.has_errors():
            raise ValueError(entity.notification.errors)

        self._repository.update(entity)

        return AddMediaToVideoOutput(id=entity.id)
