from app.common.observer.envent_sub_service.observer_event import ObserverEvent
from app.websocket.connection_manager import connection_manager
import asyncio


class SocketObserver(ObserverEvent):
    def __init__(self, name):
        self._name = name

    def update(self, message):
        # print(f"{self._name} received message: {message}")
        try:
            data = {
                "type_service": message["type_service"].key,
                "data": message["data"],
                "type": message["type"],
            }
            print("\nSocketObserver: ", data)
            asyncio.run(
                connection_manager.send_company_message_json(
                    str(message["company"].id), data
                )
            )
        except Exception as e:
            print("Error SocketObserver: ", e)
