import json

import pika


class MessageHandler:
    def __init__(self):
        self._handlers = {}

    def register_handler(self, name_exchange, handler):
        self._handlers[name_exchange] = handler

    def handle_message(self, channel, method, properties, body):
        try:
            message = json.loads(body.decode())
            print("message: ", method.exchange, message)
            channel.basic_publish(exchange=method.exchange,
                                  routing_key=properties.reply_to,
                                  properties=pika.BasicProperties(correlation_id= \
                                                                      properties.correlation_id),
                                  body=str(message))

            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            # exchange = method.exchange
            # if exchange in self._handlers:
            #     self._handlers[exchange](message)
            # else:
            #     try:
            #
            #         subject_event.notify(data_save)
            #     except Exception as e:
            #         print("Error sss: ", e)
        except Exception as e:
            channel.basic_publish(exchange='',
                                  routing_key=properties.reply_to,
                                  properties=pika.BasicProperties(correlation_id= \
                                                                      properties.correlation_id),
                                  body=str(e))
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            print("Error handle_message: ", e)
