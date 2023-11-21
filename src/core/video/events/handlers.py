from core._shared.events.event_handler import IEventHandler
from core.video.application.add_media_to_video_use_case import AddMediaToVideoUseCase, AddMediaToVideoInput
from core.video.domain.entity.value_objects import AudioVideoMedia
from core.video.domain.events import VideoUploaded
from core.video.infrastructure.video_django_app.repositories import VideoDjangoRepository


class HandleVideoUploaded(IEventHandler):
    def handle(self, event: VideoUploaded) -> None:
        print(f"Handling event: {event.type} with payload {event.payload}")
        print("Fetching video entity from repository")
        repository = VideoDjangoRepository()
        video_entity = repository.get_by_id(event.payload["video_id"])
        video_media = AudioVideoMedia(
            id=event.payload["video_id"],
            checksum=event.payload["media_checksum"],
            name=event.payload["media_name"],
            raw_location=event.payload["media_raw_location"],
            encoded_location=event.payload["media_encoded_location"],
        )

        add_media_to_video_use_case = AddMediaToVideoUseCase()
        request = AddMediaToVideoInput(id=video_entity.id, video=video_media)

        print("Adding media to video")
        add_media_to_video_use_case.execute(request)
        print("Video media was successfully added")
