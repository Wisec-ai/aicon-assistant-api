import json
from typing import Any
from commons.domain.repository.gcs_client import GcsClient
from commons.domain.repository.pubsub_client import PubSubClient
from commons.domain.constants.env_variables import TOPIC_DOCUMENT_PROCESSOR

class Service:
    @classmethod
    def publish_topic(cls, message: Any)-> str:
        pub_sub_client = PubSubClient(TOPIC_DOCUMENT_PROCESSOR)
        id_message = pub_sub_client.publish_message(message)
        return id_message
    
    @classmethod
    def load_data_pubsub(cls, file_name: str) -> str:
        gcs_path_file = GcsClient.save_pdf_to_bucket(file_name)

        cls.publish_topic(json.dumps({
            "path_file": gcs_path_file
        }))
        return gcs_path_file