import time

import pika

from app.common.constants.rabbitmq_constants import queue_data
from app.common.utils.logger import logger
from app.core.config import settings
from app.rabbitmq.message_handler import MessageHandler


class PikaListener:
    def __init__(self, exchange_type):
        self.exchange_type = exchange_type

    def __call__(self, cls):
        def __init__(self, *args, **kwargs):
            super(cls, self).__init__(*args, **kwargs)
            pass

        def start_init(self):
            try:
                self.credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
                self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST,
                                                                                     port=settings.RABBITMQ_PORT,
                                                                                     heartbeat=60,
                                                                                     credentials=self.credentials))
                self._channel = self._connection.channel()
                logger.info(f'Connected pika consumer to {settings.RABBITMQ_HOST}')

                for exchange_name in queue_data:
                    self.add_exchange(exchange_name, queue_data[exchange_name], self.message_handler.handle_message)

                try:
                    self._channel.queue_delete(queue='CHECK_STATUS_SERVER_QUEUE')
                except Exception as e:
                    pass

                name_queue = "CHECK_STATUS_SERVER_QUEUE"
                name_exchange = "CHECK_STATUS_SERVER_EXCHANGES"
                self.add_exchange_ttl(name_exchange, name_queue, self.message_handler.handle_message, 5000)
                self.add_exchange_ttl("CHECK_INFO_SERVER_EXCHANGES", "CHECK_INFO_SERVER_QUEUE", self.message_handler.handle_message, 3000)

                logger.info(' [*] Waiting for messages on queue.')
            except Exception as e:
                # logger.exception(e)
                print("Error: ", e)

        def add_exchange_ttl(self, exchange_name, queue_name, handle_message, ttl):
            self._channel.exchange_declare(exchange=exchange_name, exchange_type=self.exchange_type)
            self._channel.queue_declare(queue=queue_name, arguments={'x-message-ttl': ttl})
            self._channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key='')
            self._channel.basic_consume(queue=queue_name,
                                        on_message_callback=handle_message,
                                        auto_ack=False)

        def add_exchange(self, exchange_name, queue_name, handle_message):
            self._channel.exchange_declare(exchange=exchange_name, exchange_type=self.exchange_type)
            self._channel.queue_declare(queue=queue_name)
            self._channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key='')
            self._channel.basic_consume(queue=queue_name,
                                        on_message_callback=handle_message,
                                        auto_ack=False)

        def listen(self):
                while True:
                    try:
                        self.start_init()
                        self._channel.start_consuming()
                    except Exception as e:
                        # logger.exception(e)
                        print("Error: ", e)
                        time.sleep(5)

        def stop(self):
            self._channel.stop_consuming()
            self._connection.close()

        def __del__(self):
            self.stop()

        cls.message_handler = MessageHandler()
        cls.__init__ = __init__
        cls.listen = listen
        cls.start_init = start_init

        cls.add_exchange = add_exchange
        cls.add_exchange_ttl = add_exchange_ttl
        cls.stop = stop
        return cls
