from google.cloud import pubsub_v1
from commons.domain.constants.env_variables import PROJECT_ID

class PubSubClient:
    def __init__(self, topic_id: str) -> None:
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(PROJECT_ID, topic_id)

    def publish_message(self, message: str) -> str:
        try:
            return self.publisher.publish(self.topic_path, message.encode("utf-8")).result()
        except Exception as error:
            print(f"Error to publish message {error}")
            raise error