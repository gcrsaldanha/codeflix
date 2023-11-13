from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from core.video.domain.entities import Video


class VideoRepositoryInterface(ABC):
    @abstractmethod
    def create(self, video: Video) -> None:
        pass

    @abstractmethod
    def get_by_id(self, video_id: UUID) -> Optional[Video]:
        pass

    @abstractmethod
    def update(self, video: Video) -> None:
        pass

    @abstractmethod
    def delete(self, video_id: UUID) -> None:
        pass
