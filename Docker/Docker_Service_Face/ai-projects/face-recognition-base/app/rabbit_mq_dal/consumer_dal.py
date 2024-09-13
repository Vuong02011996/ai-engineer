import json
import pika
from threading import Event, Thread
import time

ip_rabbitMQ_server = '192.168.105.250'
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
        self.message = None  # Variable to store the message
        self.event = Event()  # Event to signal message reception
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, properties, body):
        self.message = json.loads(body)
        print("Received:", self.message)
        print("Time: ", time.time())
        self.event.set()  # Signal that a message was received

    def start_consuming(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def start(self):
        thread = Thread(target=self.start_consuming)
        thread.start()

    def close(self):
        self.connection.close()

    def get_message(self):
        self.event.wait()  # Wait until a message is received
        self.event.clear()  # Reset the event for the next message
        return self.message


if __name__ == "__main__":
    consumer = PikaConsumer(queue_name='queue_name', exchange_name='HEAD_DETECTION_EXCHANGES', exchange_type='fanout')
    consumer.start()  # Start the consuming in a separate thread
    data = consumer.get_message()  # This will block until a message is received
    print("Processed Data:", data)
    # 1724390539 - 1724390259 = 280 (562/280 = 2FPS)
    # 1724403824 - 1724404094 -
