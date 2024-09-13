from app.common.observer.envent_sub_service.save_data_observer import SaveDataObserver
from app.common.observer.envent_sub_service.socket_observer import SocketObserver
from app.common.observer.envent_sub_service.webhook_observer import WebhookObserver
from app.common.observer.envent_sub_service.vms_observer import VMSObserver
import threading


class SubjectEvent:
    def __init__(self):
        self._observers = []
        self.attach(SocketObserver("SocketObserver"))
        self.attach(WebhookObserver("WebhookObserver"))
        self.attach(VMSObserver("VMSObserver"))
        self.attach(SaveDataObserver("SaveDataObserver"))

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message: dict):
        for observer in self._observers:
            message_sent = {**message}
            threading.Thread(target=observer.update, args=(message_sent,)).start()
            # observer.update(message_sent)


subject_event = SubjectEvent()
