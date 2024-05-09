import json
import pika


ip_rabbitMQ_server = '192.168.105.250'
# ip_rabbitMQ_server = '192.168.111.98'
port_rabbitMQ_server = 5672


class PikaConsumer:
    def __init__(self, queue_name, exchange_name, exchange_type):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.credentials = pika.PlainCredentials('guest', 'guest')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip_rabbitMQ_server, port=port_rabbitMQ_server,
                                                                             credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        print("Received:", message)

    def start_consuming(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    consumer = PikaConsumer(queue_name='queue_name', exchange_name='FACE_RECOGNITION_EXCHANGES', exchange_type='fanout')
    consumer.start_consuming()
