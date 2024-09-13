import os
import time
import logging
from io import BytesIO
from app.core.config import settings
from app.services.minio_services import minio_services
from app.services.event_services.dahua.dahua_base import DahuaBase

logger = logging.getLogger("FR")


class FaceRecognition(DahuaBase):
    def __init__(self, config: dict):
        import random

        super().__init__(config)
        # Setting from request
        self.name = f"Face Recognition Camera {random.randint(1, 1000)}"
        self.code = "[FaceRecognition]"
        self.rbmq_exchange = "FACE_RECOGNITION_EXCHANGES"
        self.construct_url()

    def custom_decode(self, content: dict):
        print("Custom decode, content: ", content)
        timestamp = int(content.get("UTC", 0))
        if timestamp == 0:
            return {}
        timestamp = timestamp - 7 * 3600  # UTC+7
        try:
            with open(f"temp/fr_{timestamp}.json", "w") as f:
                f.write(str(content), indent=4)
        except Exception as e:
            print(f"Error writing file: {e}")
        if "Candidates" in content:
            candidate: list[dict] = content.get("Candidates", [{}])
            if len(candidate) > 0:  # If there is a candidate
                person: dict = candidate[0].get("Person", {})
                if person != {}:
                    user_id = person.get("UID", "")
                    if user_id != "":
                        face_bounding_box: list[dict] = content.get("Faces", [{}])
                        if face_bounding_box != {}:
                            face_bounding_box = face_bounding_box[0].get(
                                "BoundingBox", [0, 0, 0, 0]
                            )
                            data = {
                                "timestamp": timestamp,
                                "user_id": user_id,
                                "bounding_box": face_bounding_box,
                            }
        elif "Faces" in content:  # If there is no candidate but there is a face
            faces: list[dict] = content.get("Faces", [{}])
            if len(faces) > 0:
                face: dict = faces[0]
                face_bounding_box = face.get("BoundingBox", [0, 0, 0, 0])
                data = {"timestamp": timestamp, "bounding_box": face_bounding_box}
        if data and data != {}:
            logger.info(f"\nCustom decode: {data}\n")
            return data
        return {}

    def crop_face(self, image_path, bbox: list):
        from PIL import Image

        # Open the image
        if bbox == [0, 0, 0, 0]:
            return False
        image = Image.open(image_path)

        # First crop the infor bar on the top
        width, height = image.size

        left_top_remap = (int(bbox[0]) / 8192, int(bbox[1]) / 8192)
        right_bottom_remap = (int(bbox[2]) / 8192, int(bbox[3]) / 8192)
        left_top_remap = (
            int(left_top_remap[0] * width),
            int(left_top_remap[1] * height),
        )
        right_bottom_remap = (
            int(right_bottom_remap[0] * width),
            int(right_bottom_remap[1] * height),
        )

        # The crop rectangle, as a (left, upper, right, lower)-tuple.
        crop_rectangle = (
            left_top_remap[0] * 0.9,
            left_top_remap[1] * 0.9,
            right_bottom_remap[0] * 1.1,
            right_bottom_remap[1] * 1.1,
        )

        # Perform the crop
        cropped_image = image.crop(crop_rectangle)

        # Convert the cropped image to bytes
        img_byte_arr = BytesIO()
        cropped_image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        # Save or display the cropped image
        crop_name = f"crop_fr_{int(time.time())}"
        temp_image_name, temp_image_path = super().save_temp_image(
            img_byte_arr, crop_name
        )
        if temp_image_name and temp_image_path:
            crop_url = minio_services.upload_file(
                temp_image_path, temp_image_name, bucket=settings.BUCKET_FACE
            )
            os.remove(temp_image_path)
            return crop_url

    def custom_data_to_send(self, data: dict, image):
        event_time = data.get("timestamp", int(time.time()))
        filename = f"dh_fr_{event_time}"
        if "user_id" not in data:
            filename = f"dh_fr_unknown_{event_time}"
        _, temp_image_path = super().save_temp_image(image, filename)
        if "bounding_box" in data:
            image_url = self.crop_face(temp_image_path, data["bounding_box"])
            # del data["face_bounding_box"]
        else:
            image_url = False
        if "user_id" not in data and not image_url:  # No face detected
            return {}
        data["image_url"] = image_url
        try:
            os.remove(temp_image_path)
        except Exception:
            print(f"Error removing {temp_image_path}")
        logger.info("Custom data: ", data)
        return data
