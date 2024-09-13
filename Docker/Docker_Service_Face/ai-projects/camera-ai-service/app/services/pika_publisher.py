import json
import logging
from app.core.config import settings
from kombu import Connection, Exchange

# Set Pika's logging level to ERROR to suppress INFO logs
logging.getLogger("pika").setLevel(logging.ERROR)

LOGGER = logging.getLogger("pika_logger")
LOGGER.setLevel(logging.ERROR)


class PikaPublisher:
    exchanges = {}

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PikaPublisher, cls).__new__(cls)
        return cls.instance

    def connect(self):
        self.connection = Connection(
            f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}//"
        )

    def send_message(self, data, exchange_name=None):
        try:
            if exchange_name not in self.exchanges:
                self.exchanges[exchange_name] = Exchange(exchange_name, "fanout")
            message = json.dumps(data)
            with self.connection.Producer() as producer:
                producer.publish(
                    body=message,
                    exchange=self.exchanges[exchange_name],
                    routing_key="",
                    retry=True,
                    retry_policy={
                        "interval_start": 0,  # First retry immediately,
                        "interval_step": 2,  # then increase by 2s for every retry.
                        "interval_max": 30,  # but don't exceed 30s between retries.
                        "max_retries": 30,  # give up after 30 tries.
                    },
                )
        except Exception as e:
            LOGGER.debug("Error occurred while sending message: %s" + str(e))
            self.connect()

    def close(self):
        self.connection.close()
        self.connection.release()

    def send_to_rbmq(self, data, exchange_name):
        try:
            self.send_message(data=data, exchange_name=exchange_name)
            logging.info(f"\nSend rabbitmq: {data}\n")
        except Exception as e:
            LOGGER.debug("Error occurred while sending message: %s" + str(e))


pika_publisher = PikaPublisher()
