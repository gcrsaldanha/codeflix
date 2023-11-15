from abc import ABC, abstractmethod
from uuid import UUID

from core.video.domain.value_objects import MediaResource, MediaType, AudioVideoMedia, ImageMedia


class StorageServiceInterface(ABC):
    @abstractmethod
    def store_video(self, resource: MediaResource, video_id: UUID) -> AudioVideoMedia:
        pass

    @abstractmethod
    def store_image(self, resource: MediaResource, video_id: UUID) -> ImageMedia:
        pass

    @abstractmethod
    def fetch(self, video_id: UUID, media_type: MediaType) -> MediaResource | None:
        pass

    @abstractmethod
    def remove(self, media_resource: MediaResource, video_id: UUID) -> None:
        pass

    @abstractmethod
    def remove_all(self, video_id: UUID) -> None:
        pass
