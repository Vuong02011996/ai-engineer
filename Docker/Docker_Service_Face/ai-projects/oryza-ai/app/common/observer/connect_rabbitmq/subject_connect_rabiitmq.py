from app.common.observer.connect_rabbitmq.check_connect_server import check_connect_observer
from app.common.observer.connect_rabbitmq.observer_connect_rabiitmq import ObserverConnectRabbitMQ


class SubjectConnectRabbitMQ:
    def __init__(self):
        self._observers = []

    def attach(self, observer: ObserverConnectRabbitMQ):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: ObserverConnectRabbitMQ):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)


# Sử dụng
subject_connect_rabbitmq = SubjectConnectRabbitMQ()
subject_connect_rabbitmq.attach(check_connect_observer)