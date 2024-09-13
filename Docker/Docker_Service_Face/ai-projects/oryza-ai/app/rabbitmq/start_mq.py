import threading

from app.common.constants.rabbitmq_constants import (
    CHECK_STATUS_SERVER_EXCHANGES, CHECK_INFO_SERVER_EXCHANGES,
)
from app.rabbitmq.mq_service import MQService


class StartMQ:
    def __init__(self):
        pass

    @staticmethod
    def init_queue():
        mq_service = MQService()
        # mq_service.message_handler.register_handler(FACE_RECOGNITION_EXCHANGES, mq_service.get_face_recognition_message)
        # mq_service.message_handler.register_handler(IDENTIFY_UNIFORMS_EXCHANGES,
        #                                             mq_service.get_identify_uniforms_message)
        # mq_service.message_handler.register_handler(CROWD_DETECTION_EXCHANGES, mq_service.get_crowd_detection_message)
        # mq_service.message_handler.register_handler(PLATE_NUMBER_EXCHANGES, mq_service.get_plate_number)
        mq_service.message_handler.register_handler(
            CHECK_STATUS_SERVER_EXCHANGES, mq_service.check_status_server
        )
        mq_service.message_handler.register_handler(
            CHECK_INFO_SERVER_EXCHANGES, mq_service.check_info_server
        )

        mq_service.listen()

    def start(self):
        t = threading.Thread(target=self.init_queue, daemon=True)
        t.start()
