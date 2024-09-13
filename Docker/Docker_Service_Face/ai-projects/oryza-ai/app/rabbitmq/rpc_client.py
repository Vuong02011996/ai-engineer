import json
import time

import pika
import uuid

from app.core.config import settings


class PersonRpcClient(object):

    def __init__(self):
        self.credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT,
                                      credentials=self.credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = json.dumps(message)

        self.channel.basic_publish(
            exchange='create_person_exchange',
            routing_key='create_person_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message)
        start_time = time.time()
        while self.response is None:
            # if time.time() - start_time > 5:
            #     break
            self.connection.process_data_events()
        return self.response

# fibonacci_rpc = FibonacciRpcClient()
# response = fibonacci_rpc.call({"id": "6618d6604a553afe2ad70695", "type_server": "661c9267a7703f682a7caf72"})
# print(" [.] Got %r" % response)
