import pika

from app.core.config import settings
from app.rpc_server.message_handler import MessageHandler


class PikaListener:
    def __init__(self):
        pass

    def __call__(self, cls):
        def __init__(self, *args, **kwargs):
            super(cls, self).__init__(*args, **kwargs)
            self.credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST,
                                                                                 port=settings.RABBITMQ_PORT,
                                                                                 credentials=self.credentials))
            self._channel = self._connection.channel()



            name_queue = "create_person_queue"
            name_exchange = "create_person_exchange"
            self._channel.exchange_declare(exchange=name_exchange)
            self._channel.queue_declare(queue=name_queue, arguments={'x-message-ttl': 5000})
            self._channel.queue_bind(queue=name_queue, exchange=name_exchange, routing_key=name_queue)
            self._channel.basic_qos(prefetch_count=1)
            self._channel.basic_consume(queue=name_queue,
                                        on_message_callback=self.message_handler.handle_message,
                                        auto_ack=False)


        def add_exchange(self, exchange_name, queue_name, handle_message):
            self._channel.exchange_declare(exchange=exchange_name)
            self._channel.queue_declare(queue=queue_name)
            self._channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key='')
            self._channel.basic_consume(queue=queue_name,
                                        on_message_callback=handle_message,
                                        auto_ack=False)

        def listen(self):
            try:
                self._channel.start_consuming()
            except KeyboardInterrupt as e:
                pass
            except Exception as e:
                pass

        def stop(self):
            self._channel.stop_consuming()
            self._connection.close()

        def __del__(self):
            self.stop()

        cls.message_handler = MessageHandler()
        cls.message_handler = MessageHandler()
        cls.__init__ = __init__
        cls.listen = listen
        cls.add_exchange = add_exchange
        cls.stop = stop
        return cls
