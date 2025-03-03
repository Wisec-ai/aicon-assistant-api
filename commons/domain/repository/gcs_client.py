from typing import Dict, Any
import gcsfs
from commons.domain.constants.env_variables import PROJECT_ID, MKTCLOUD_BUCKET
import json
import time
from constants import MIDDLE_PATH_DIRECTORY

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

        json_path = f"gs://{MKTCLOUD_BUCKET}/{path_directory}/{json_file_name}.json"

        gcs_file_system = gcsfs.GCSFileSystem(project=PROJECT_ID)
        start_time = time.time()
        with gcs_file_system.open(json_path, 'w') as f:
            json.dump(data, f)
        print(f"Upload Json File {time.time() - start_time}")
        return json_path