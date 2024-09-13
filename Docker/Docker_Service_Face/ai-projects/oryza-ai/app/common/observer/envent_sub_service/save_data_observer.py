from app.common.constants.rabbitmq_constants import (
    loitering,
    illegal_parking,
)
from app.common.observer.envent_sub_service.observer_event import ObserverEvent
from app.schemas.event_schemas import EventCreate
from app.services.event_services import event_services
from app.models import TypeService


class SaveDataObserver(ObserverEvent):
    def __init__(self, name):
        self._name = name

    def update(self, message):
        # print(f"{self._name} received message: {data_save}")
        try:
            type = message["type"]
            type_service: TypeService = message["type_service"]
            del message["type"]
            del message["process"]
            if type_service.key in [loitering, illegal_parking] and type == "update":
                print("\nSaveDataObserver: ", message)
                data_save2 = message["data"]
                id_camera = str(message["camera"].id)
                if type_service.key == loitering:
                    event_services.update_loitering_detection(
                        data_save2["end_time"],
                        data_save2["image_end"],
                        id_camera,
                        data_save2["track_id"],
                        data_save2["duration_time"],
                    )
                elif type_service.key == illegal_parking:
                    event_services.update_illegal_parking(
                        data_save2["end_time"],
                        data_save2["image_end"],
                        id_camera,
                        data_save2["track_id"],
                        data_save2["duration_time"],
                        data_save2["status"],
                    )
            else:
                message["camera"] = str(message["camera"].id)
                event_services.create(obj_in=EventCreate(**message))
        except Exception as e:
            print("Error SaveDataObserver: ", e)
