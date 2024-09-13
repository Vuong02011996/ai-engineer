import json
import pika
import os

ip_rabbitMQ_server = os.getenv("ip_rabbitMQ_server")
port_rabbitMQ_server = int(os.getenv("port_rabbitMQ_server"))


class PikaPublisher:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PikaPublisher, cls).__new__(cls)
            cls.instance.startD('CHECK_STATUS_SERVER_EXCHANGES', 'fanout')
        return cls.instance

    def startD(self, exchange_name, exchange_type):
        self.credentials = pika.PlainCredentials('guest', 'guest')
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=ip_rabbitMQ_server, port=port_rabbitMQ_server,
                                                                             credentials=self.credentials))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self._exchange_name = exchange_name

    def send_message(self, data, exchange_name=None):
        if exchange_name == None:
            exchange_name = self._exchange_name
        message = json.dumps(data)
        self._channel.basic_publish(exchange=exchange_name, routing_key='', body=message)

    def close(self):
        self._connection.close()



if __name__ == '__main__':
    pikaPublisher = PikaPublisher()
    data_send = {'ip': '192.168.111.98', 'port': 30000,
                 'data': {'9a5dcef8-8028-5c36-56b9-ee51381f454d': False}}
    pikaPublisher.send_message(data=data_send, exchange_name='CHECK_STATUS_SERVER_EXCHANGES')