from google.cloud import storage
from google.oauth2 import service_account

from core.video.domain.storage_service_interface import StorageServiceInterface
from core.video.domain.value_objects import MediaResource, MediaType
from uuid import UUID


# Temporary implementation: Generated by ChatGPT from StorageServiceInterface
# Made a few adjustments to use MeidaResource/Resource
# TODO: update so that store methods return the AudioVideoMedia / ImageMedia
class GCPStorageService(StorageServiceInterface):
    def __init__(self, bucket_name, credentials_file_path):
        self.client = self._create_gcp_storage_client(credentials_file_path)
        self.bucket = self.client.bucket(bucket_name)

    def _create_gcp_storage_client(self, credentials_file_path):
        credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
        return storage.Client(credentials=credentials)

    def store_video(self, resource: MediaResource, video_id: UUID) -> None:
        blob = self.bucket.blob(str(video_id) + '/' + resource.resource.name)
        blob.upload_from_string(resource.resource.content, content_type=resource.resource.content_type)

    def fetch(self, video_id: UUID, media_type: MediaType) -> MediaResource:
        blob = self.bucket.blob(str(video_id) + '/' + media_type.value)
        content = blob.download_as_text()
        return MediaResource(content, media_type.value)

    def remove(self, media_resource: MediaResource, video_id: UUID) -> None:
        blob = self.bucket.blob(str(video_id) + '/' + media_resource.resource.name)
        blob.delete()

    def remove_all(self, video_id: UUID) -> None:
        # Delete all blobs related to the video ID
        blobs = self.bucket.list_blobs(prefix=str(video_id) + '/')
        for blob in blobs:
            blob.delete()
