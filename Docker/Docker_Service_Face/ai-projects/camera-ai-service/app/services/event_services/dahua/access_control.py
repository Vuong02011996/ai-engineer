import os
import time
import logging
import json
from app.core.config import settings
from app.services.minio_services import minio_services
from app.services.event_services.dahua.dahua_base import DahuaBase

logger = logging.getLogger("AC")


class AccessControl(DahuaBase):
    def __init__(self, config: dict):
        import random

        super().__init__(config)
        # Setting from request
        self.name = f"Access Control {random.randint(1, 1000)}"
        self.code = "[AccessControl]"
        self.rbmq_exchange = "FACE_RECOGNITION_EXCHANGES"
        self.construct_url()

    def custom_decode(self, content: dict):
        user_id = content.get("UserID", "")
        timestamp = int(content.get("UTC", 0))
        if timestamp == 0:
            return {}
        if user_id == "":
            data = {"timestamp": timestamp}  # For fast-adding unknown person
        else:
            data = {"user_id": user_id, "timestamp": timestamp}
        logger.info(f"Custom decode: {json.dumps(data)}")
        return data

    def custom_data_to_send(self, data: dict, image):
        event_time = data.get("timestamp", int(time.time()))
        filename = f"dh_ac_{event_time}"
        if "user_id" not in data:
            filename = f"dh_ac_unknown_{event_time}"
        temp_image_name, temp_image_path = super().save_temp_image(image, filename)
        if temp_image_path and temp_image_name:  # If image is saved successfully
            data["image_url"] = minio_services.upload_file(
                temp_image_path, temp_image_name, bucket=settings.BUCKET_FACE
            )
            try:
                os.remove(temp_image_path)
            except Exception:
                pass
        logger.info(f"Custom data to send: {json.dumps(data)}")
        return data
