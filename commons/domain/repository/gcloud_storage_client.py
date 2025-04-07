import mimetypes
from google.cloud import storage
from commons.domain.constants.env_variables import DOCUMENT_BUCKET, DEFAULT_SUB_FOLDERS
from commons.domain.constants.domain_constants import DEFAULT_EXPIRATION_TIME, DEFAULT_MIMETYPE
from datetime import timedelta

class GCloudStorageClient:
    def __init__(self) -> None:
        self.storage_client = storage.Client()
    def _get_mime_type(self, file_name: str) -> str:
        content_type, _ = mimetypes.guess_type(file_name)

        if not content_type:
            return DEFAULT_MIMETYPE

        return content_type

    def generate_presigned_url(
            self,
            file_name: str,
            sub_folder: str = DEFAULT_SUB_FOLDERS,
            gcs_bucket: str = DOCUMENT_BUCKET
    ):

        bucket = self.storage_client.get_bucket(gcs_bucket)

        blob = bucket.blob(f"{sub_folder}/{file_name}")

        content_type = self._get_mime_type(file_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=DEFAULT_EXPIRATION_TIME),
            method="PUT",
            content_type=content_type,
        )

        return url

