from typing import Optional
from uuid import UUID

from django.db.models import QuerySet

from core.video.domain.entities import Video
from core.video.domain.video_repository import VideoRepositoryInterface
from core.video.infrastructure.video_django_app.models import Video as VideoModel


class VideoDjangoRepository(VideoRepositoryInterface):
    def __init__(self, queryset: Optional[QuerySet[VideoModel]] = None):
        self._queryset = queryset or VideoModel.objects.all()

    def create(self, video: Video) -> None:
        self._queryset.create(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            opened=video.opened,
            published=video.published,
            rating=video.rating,
            categories=video.categories,
            genres=video.genres,
            cast_members=video.cast_members,
            banner=video.banner,
            thumbnail=video.thumbnail,
            thumbnail_half=video.thumbnail_half,
            trailer=video.trailer,
            video=video.video,
        )

    def get_by_id(self, video_id: UUID) -> Optional[Video]:
        pass

    def update(self, video: Video) -> None:
        pass

    def delete(self, video_id: UUID) -> None:
        pass
