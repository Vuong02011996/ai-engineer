import json

import requests
from odmantic import ObjectId

from app.common.constants.rabbitmq_constants import (
    FACE_RECOGNITION_EXCHANGES,
    loitering,
    illegal_parking,
    plate_number,
)
from app.common.observer.envent_sub_service.subject_envent import subject_event
from app.common.utils.logger import logger
from app.core.config import settings
from app.services.event_services import type_service_services
from app.services.process_services import process_services


class MessageHandler:
    def __init__(self):
        self._handlers = {}

    def register_handler(self, name_exchange, handler):
        self._handlers[name_exchange] = handler

    def handle_message(self, channel, method, properties, body):
        try:
            message = json.loads(body.decode())
            # print("message: ", method.exchange, message)
            if method.exchange != "CHECK_INFO_SERVER_EXCHANGES":
                logger.info(f" [✓] message {method.exchange} {message}")

            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            exchange = method.exchange
            if exchange in self._handlers:
                # logger.warning(f' [✓] message forwarded <successfully> to MQ Service for processing from MessageHandler..')
                self._handlers[exchange](message)
            else:
                try:
                    if (
                        "id" not in message
                        or "data" not in message
                        or ObjectId.is_valid(message["id"]) is False
                    ):
                        # print("message not found id or data")
                        return

                    process = process_services.get(id=message["id"])
                    if not process:
                        logger.error(" [x] process not found")
                        return
                    camera = process.camera
                    if not camera:
                        logger.error(" [x] camera not found")
                        return
                    type_service = type_service_services.get_type_service(
                        id=process.id_type_service
                    )
                    if not type_service:
                        logger.error(" [x] type_service not found")
                        return

                    type = "insert"
                    if type_service.key == FACE_RECOGNITION_EXCHANGES:
                        # print("data: ", message["data"])
                        if "user_id" in message["data"]:
                            user_id = message["data"]["user_id"]
                            url = f"{settings.SERVER_FACE}/person/get_by_person_id_camera/{user_id}"
                            data_face = requests.get(url)
                            data_face = data_face.json()
                            if not data_face:
                                logger.error(" [x] data_face not found")
                                message["data"]["user_id"] = "Unknown"
                                message["data"]["name"] = "Unknown"
                            else:
                                message["data"]["user_id"] = data_face["id"]
                                message["data"]["name"] = data_face["name"]
                        else:
                            message["data"]["user_id"] = "Unknown"
                            message["data"]["name"] = "Unknown"
                    elif type_service.key == loitering:
                        if "duration_time" not in message["data"]:
                            message["data"]["start_time"] = message["data"]["timestamp"]
                            del message["data"]["timestamp"]
                            message["data"]["end_time"] = -1
                            message["data"]["duration_time"] = -1
                            image_start = message["data"]["image_url"]
                            message["data"]["image_start"] = image_start
                            message["data"]["image_end"] = ""
                            del message["data"]["image_url"]
                        else:
                            message["data"]["end_time"] = message["data"]["timestamp"]
                            type = "update"
                            image_end = message["data"]["image_url"]
                            message["data"]["image_end"] = image_end
                            del message["data"]["timestamp"]
                            del message["data"]["image_url"]
                    elif type_service.key == illegal_parking:
                        if "duration_time" not in message["data"]:
                            message["data"]["start_time"] = message["data"]["timestamp"]
                            del message["data"]["timestamp"]
                            image_start = message["data"]["image_url"]
                            message["data"]["image_start"] = image_start
                            message["data"]["image_end"] = ""
                            del message["data"]["image_url"]
                        else:
                            message["data"]["end_time"] = message["data"]["timestamp"]
                            type = "update"
                            image_end = message["data"]["image_url"]
                            message["data"]["image_end"] = image_end
                            del message["data"]["timestamp"]
                            del message["data"]["image_url"]
                        print('\nmessage["data"]: ', message["data"])
                    elif type_service.key == plate_number:
                        message["data"]["video"] = ""

                    message["data"]["camera_id"] = str(camera.id)
                    message["data"]["camera_name"] = camera.name
                    message["data"]["camera_ip"] = camera.ip_address
                    data_save = {
                        "camera": camera,
                        "data": message["data"],
                        "company": camera.company,
                        "type_service": type_service,
                        "type": type,
                        "process": process,
                    }
                    # logger.info(f' [✓] data save {data_save}')
                    subject_event.notify(data_save)
                except Exception as e:
                    print("Error sss: ", e)
        except json.decoder.JSONDecodeError as e:
            # logger.error(f' [x] message forwarded <not successfully> to MQ Service for processing from MessageHandler..')
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            print("Error handle_message: ", e)
            # logger.error(f' [x] Rejected {body!r} on queue {settings.RABBITMQ_QUEUE}')
