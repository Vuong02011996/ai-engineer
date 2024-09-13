import pika
import json
import logging
from app.core.config import settings

# Set Pika's logging level to ERROR to suppress INFO logs
logging.getLogger("pika").setLevel(logging.ERROR)

LOGGER = logging.getLogger("pika_logger")
LOGGER.setLevel(logging.ERROR)


class PikaPublisher:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PikaPublisher, cls).__new__(cls)
            cls.instance.startD("FACE_RECOGNITION_EXCHANGE", "fanout")
            cls.instance.startD("CHECK_STATUS_SERVER_EXCHANGES", "fanout")
        return cls.instance

    def startD(self, exchange_name, exchange_type):
        self.credentials = pika.PlainCredentials(
            settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD
        )
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                credentials=self.credentials,
            )
        )
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type
        )
        self._exchange_name = exchange_name

    def send_message(self, data, exchange_name=None):
        try:
            if not exchange_name:
                exchange_name = self._exchange_name
            message = json.dumps(data)
            self._channel.basic_publish(
                exchange=exchange_name, routing_key="", body=message
            )
        except Exception as e:
            LOGGER.debug("Error occurred while sending message: %s" + str(e))

    def close(self):
        self._connection.close()

    def send_to_rbmq(self, data, exchange_name):
        try:
            # if not self._connection.is_open:
            #     print("Connection is closed, reconnecting...")
            self.startD(exchange_name=exchange_name, exchange_type="fanout")
            self.send_message(data=data, exchange_name=exchange_name)
            self.close()
            logging.info(f"Send rabbitmq: {data}")
        except Exception as e:
            LOGGER.debug("Error occurred while sending message: %s" + str(e))


pika_publisher = PikaPublisher()
