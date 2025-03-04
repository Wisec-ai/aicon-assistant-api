import json
import time
import gcsfs
from typing import Dict, Any
from commons.domain.constants.env_variables import PROJECT_ID, DOCUMENT_BUCKET
from commons.domain.constants.domain_constants import MIDDLE_PATH_DIRECTORY

class GcsClient:
    def __init__(self) -> None:
        pass

    @classmethod
    def read_json_from_bucket(cls, json_path: str) -> Dict[str, Any]:
        json_data = {}
        
        gcs_file_system = gcsfs.GCSFileSystem(project=PROJECT_ID)
        start_time = time.time()
        with gcs_file_system.open(json_path) as f:
            json_data = json.load(f)
        print(f"Download Json File {time.time() - start_time}")
        return json_data

    @classmethod
    def save_json_to_bucket(cls, json_file_name: str, data: Dict[str, Any], path_directory: str = MIDDLE_PATH_DIRECTORY ) -> Dict[str, Any]:

        json_path = f"gs://{DOCUMENT_BUCKET}/{path_directory}/{json_file_name}.json"

        gcs_file_system = gcsfs.GCSFileSystem(project=PROJECT_ID)
        start_time = time.time()
        with gcs_file_system.open(json_path, 'w') as f:
            json.dump(data, f)
        print(f"Upload Json File {time.time() - start_time}")
        return json_path

    @classmethod
    def save_pdf_to_bucket(cls, file_name: str, data: Dict[str, Any], path_directory: str = MIDDLE_PATH_DIRECTORY ) -> Dict[str, Any]:
        
        gcs_file_system = gcsfs.GCSFileSystem(project=PROJECT_ID)
        start_time = time.time()

        pdf_path = f"{DOCUMENT_BUCKET}/{path_directory}/{file_name}"

        with gcs_file_system.open(pdf_path, 'wb') as gcs_file:
            with open(file_name, 'rb') as local_file:
                gcs_file.write(local_file.read())
        
        print(f"Upload Pdf File {time.time() - start_time}")
        return pdf_path