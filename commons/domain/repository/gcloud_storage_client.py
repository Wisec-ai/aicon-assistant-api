from google.cloud import storage
from commons.domain.constants.env_variables import DOCUMENT_BUCKET, DEFAULT_SUB_FOLDERS
from commons.domain.constants.domain_constants import DEFAULT_EXPIRATION_TIME
from datetime import timedelta

class GCloudStorageClient:
    def __init__(self) -> None:
        self.storage_client = storage.Client()
        
    def generate_presigned_url(
            self,
            file_name: str,
            sub_folder: str = DEFAULT_SUB_FOLDERS,
            gcs_bucket: str = DOCUMENT_BUCKET
    ):

        bucket = self.storage_client.get_bucket(gcs_bucket)

        blob = bucket.blob(f"{sub_folder}/{file_name}")

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=DEFAULT_EXPIRATION_TIME),
            method="PUT",
            content_type="application/pdf",
        )

        return url

