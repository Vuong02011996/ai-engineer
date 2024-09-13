import re
import logging
import os
from io import BytesIO
import time
from app.services.pika_publisher import pika_publisher
from app.services.minio_services import minio_services
from app.core.config import settings

logger = logging.getLogger("kbvision_plate_detection")


class KBVisionPlateDetection:
    def __init__(self, config: dict):
        # Setting from request
        self.name = "KBVision Plate Detection Camera"
        self.username = config["username"]
        self.password = config["password"]
        self.ip_address = config["ip_address"]
        self.port = config["port"]
        self.process_id = config["process_id"]

        # Dahua Camera default settings
        self.channel = 1
        self.auth = "digest"
        self.protocol = "http"
        self.alerts = True
        self.basetopic = "CameraEvents"
        self.url = f"http://{self.ip_address}:{self.port}/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[TrafficJunction]"
        self.isNVR = True

        # DahuaBT Camera connection settings
        self.CurlObj = None
        self.Connected = None
        self.Reconnect = None
        self.MQTTConnected = None

        self.pika_publisher = pika_publisher
        self.buffer = b""
        self.boundary = b"--myboundary"

    # Connected to camera
    def OnConnect(self):
        logger.debug(f"[{self.name}] OnConnect()")
        self.Connected = True

    # disconnected from camera
    def OnDisconnect(self, reason):
        logger.debug(f"[{self.name}] OnDisconnect({reason})")
        self.Connected = False

    # on receive data from camera.
    def OnReceive(self, data):
        self.buffer += data

        while self.boundary in self.buffer:
            start_index = self.buffer.find(self.boundary)
            end_index = self.buffer.find(
                self.boundary, start_index + len(self.boundary)
            )
            if end_index != -1:
                # Extract the message
                message = self.buffer[start_index:end_index]
                self.process_message(message)

                # Remove the processed message from the buffer
                self.buffer = self.buffer[end_index:]
            else:
                # If no complete message, break the loop and wait for more data
                break

    def process_message(self, message):
        # Find the end of the headers
        header_end_index = message.find(b"\r\n\r\n") + 4
        # Decode only the headers part to extract information
        headers = message[:header_end_index].decode("utf-8")

        # Extract content type and content length
        content_type_match = re.search(r"Content-Type: ([\w/]+)", headers)
        content_length_match = re.search(r"Content-Length: (\d+)", headers)

        if content_type_match and content_length_match:
            content_type = content_type_match.group(1)
            content_length = int(content_length_match.group(1))

            # Calculate the start index of the actual content
            # header_end_index = message.find(b'\r\n\r\n') + 4  # Assuming headers end with double CRLF
            actual_content = message[
                header_end_index : header_end_index + content_length
            ]

            # Determine the file extension and save the content
            if content_type == "text/plain":
                self.process_text_content(actual_content)
            elif content_type == "image/jpeg":
                self.process_image_content(actual_content)
            else:
                logger.warning(f"Unsupported content type: {content_type}")
        else:
            logger.warning("Content-Type or Content-Length not found in message")

    def process_text_content(self, content):
        decode_content: str = content.decode("utf-8")
        decode_content = decode_content.split("\r\n")
        temp_data = {}
        vehicle_bounding_box = [0, 0, 0, 0]
        plate_bounding_box = [0, 0, 0, 0]
        for content in decode_content:
            if content.startswith("Events[0].UTC="):
                temp_data["timestamp"] = str(int(content.split("=")[1]) - 7 * 3600)
            if content.startswith("Events[0].TrafficCar.PlateNumber="):
                temp_data["license_plate"] = content.split("=")[1]
            elif content.startswith("Events[0].TrafficCar.VehicleBoundingBox"):
                index = content.split("Events[0].TrafficCar.VehicleBoundingBox[")[
                    1
                ].split("]")[0]
                vehicle_bounding_box[int(index)] = int(content.split("=")[1])
            elif content.startswith("Events[0].TrafficCar.BoundingBox"):
                index = content.split("Events[0].TrafficCar.BoundingBox[")[1].split(
                    "]"
                )[0]
                plate_bounding_box[int(index)] = int(content.split("=")[1])
            elif content.startswith("Events[0].CommInfo.SnapCategory="):
                temp_data["brand_name"] = content.split("=")[1]
            elif content.startswith("Events[0].TrafficCar.VehicleColor="):
                temp_data["vehicle_color"] = content.split("=")[1]
            elif content.startswith("Events[0].TrafficCar.VehicleSign="):
                temp_data["vehicle_type"] = content.split("=")[1]
        temp_data["license_plate_bounding_boxes"] = plate_bounding_box
        temp_data["vehicle_bounding_box"] = vehicle_bounding_box
        self.temp_data_storage = temp_data

    def process_image_content(self, content):
        # Check if we have already collected the necessary text data
        if self.temp_data_storage:
            # Now we have both the image and the data, send them together
            self.send_data_and_image(self.temp_data_storage, content)
            # Clear temp_data_storage after sending
            self.temp_data_storage = {}
        else:
            # If we don't have the text data yet, just store the image temporarily
            logger.info(
                "Received image without preceding text data. Image disregarded."
            )

    def save_temp_image(self, content):
        temp_name = f"{int(time.time())}"
        try:
            path = os.path.join("./temp", temp_name + ".jpg")
            if not os.path.exists("./temp"):
                os.makedirs("./temp")
            with open(path, "wb") as f:
                f.write(content)
            return path
        except Exception as e:
            logger.error(f"Error saving image content: {e}")
            return False

    def crop_plate(self, image_path, bbox: list):
        from PIL import Image

        # Open the image
        if bbox == [0, 0, 0, 0]:
            return False
        image = Image.open(image_path)
        # First crop the infor bar on the top
        width, height = image.size
        # image = image.crop((0, 0, width, height-60))
        # width, height = image.size

        left_top_remap = (bbox[0] / 8192, bbox[1] / 8192)
        right_bottom_remap = (bbox[2] / 8192, bbox[3] / 8192)
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
            left_top_remap[0] * 0.98,
            left_top_remap[1] * 1.02,
            right_bottom_remap[0] * 1.02,
            right_bottom_remap[1] * 1.04,
        )
        # print(f"Crop rectangle: {crop_rectangle}")
        # Perform the crop
        cropped_image = image.crop(crop_rectangle)
        # Convert the cropped image to bytes
        img_byte_arr = BytesIO()
        cropped_image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()
        # Save or display the cropped image
        temp_image_path = self.save_temp_image(img_byte_arr)
        if temp_image_path:
            on_bucket_name = f"crop_{int(time.time())}.jpg"
            crop_url = minio_services.upload_file(
                temp_image_path, on_bucket_name, bucket=settings.BUCKET_PLATE
            )
            os.remove(temp_image_path)
            return crop_url
        return False

    def send_data_and_image(self, data, image):
        # If cant recognize the plate, return
        if "license_plate" not in data:
            return
        # Generate a filename based on the event time or current time if not available
        event_time = data.get("event_time", int(time.time()))
        filename = f"kbv_pd_{event_time}"
        # with open(f"{filename}.txt", "wb") as file:
        #     file.write(json.dumps(data).encode("utf-8"))
        # Save the image content to a file
        big_img_path = self.save_temp_image(image)
        # Upload the image to Minio
        data["big_img"] = minio_services.upload_file(
            big_img_path, f"{filename}.jpg", bucket=settings.BUCKET_PLATE
        )
        # Crop the plate
        data["image_url"] = self.crop_plate(
            big_img_path, data["license_plate_bounding_boxes"]
        )
        data["camera_ip"] = self.ip_address

        to_send_data = {"id": self.process_id, "data": data}
        logger.info("Data to send: " + str(to_send_data))

        # Send the data to RabbitMQ
        self.pika_publisher.send_to_rbmq(
            data=to_send_data, exchange_name="PLATE_NUMBER_EXCHANGES"
        )
        try:
            os.remove(big_img_path)
        except Exception:
            pass
