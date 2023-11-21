from typing import Optional
from uuid import UUID

from django.db.models import QuerySet

from core._shared.events.event_service import EventService
from core.video.domain.entity.video import Video
from core.video.domain.repository.video_repository_interface import VideoRepositoryInterface
from core.video.infrastructure.video_django_app.models import Video as VideoModel


class VideoDjangoRepository(VideoRepositoryInterface):
    def __init__(
        self,
        queryset: Optional[QuerySet[VideoModel]] = None,
        event_service: Optional[EventService] = None,
    ):
        self._queryset = queryset or VideoModel.objects.all()
        self._event_service = event_service or EventService()

    def create(self, video: Video) -> None:
        # TODO: this and update should dispatch the video events!
        # This can become a "gateway", which will have the repository and the EventService.send

        # TODO: persist related value objects: banner, thumbnail, video, etc.
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
            # banner=banner,
            # thumbnail=thumbnail,
            # thumbnail_half=thumbnail_half,
            # trailer=trailer,
            # video=video,
        )

        video.dispatch_events(event_service=self._event_service)

    def get_by_id(self, video_id: UUID) -> Optional[Video]:
        pass

    def update(self, video: Video) -> None:
        pass

    def delete(self, video_id: UUID) -> None:
        pass
