import asyncio

from app.common.observer.connect_rabbitmq.subject_connect_rabiitmq import (
    subject_connect_rabbitmq,
)
from app.rabbitmq.message_listener import PikaListener
from app.core.config import settings
from app.websocket.connection_manager import connection_manager
from app.websocket.web_socket_super_admin import web_socket_super_admin


@PikaListener(exchange_type=settings.RABBITMQ_EXCHANGE_TYPE)
class MQService(object):
    exchange_type = settings.RABBITMQ_EXCHANGE_TYPE

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_face_recognition_message(message):
        print(
            f"--> this message get_face_recognition_message from MQService: {message}"
        )
        if not connection_manager.active_connections:
            return
        if "id" not in message or "event_type" not in message or "data" not in message:
            return

        # data = {
        #     "camera_id": message["id"],
        #     "event_type": message["event_type"],
        #     "data": message["data"],
        # }

    @staticmethod
    def get_identify_uniforms_message(message):
        print(
            f"--> this message get_identify_uniforms_message from MQService: {message}"
        )
        # data = {"camera_id": message["id"], "type_server": message["type_server"], "data": message["data"]}
        # data_save = EventCreate(**data)
        # event_services.create(obj_in=data_save)
        # if not manager.active_connections:
        #     return
        # asyncio.run(manager.send_company_message_json("1", message))

    @staticmethod
    def get_crowd_detection_message(message):
        print(f"--> this message get_crowd_detection_message from MQService: {message}")

    @staticmethod
    def get_plate_number(message):
        # print(f"--> this message get_plate_number from MQService: {message}")
        pass

    @staticmethod
    def check_status_server(message):
        subject_connect_rabbitmq.notify(message)

    @staticmethod
    def check_info_server(message):
        asyncio.run(
            web_socket_super_admin.send_company_message_json(
                {
                    "type": "INFO_SERVER",
                    "data": message,
                }
            )
        )
