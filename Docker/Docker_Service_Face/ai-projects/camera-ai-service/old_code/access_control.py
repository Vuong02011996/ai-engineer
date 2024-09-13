import os
import re
import logging
import time
from app.services.pika_publisher import pika_publisher
from app.core.config import settings
from app.services.minio_services import minio_services

logger = logging.getLogger("access_control")


class AccessControl:
    def __init__(self, config: dict):
        # Setting from request
        self.name = "Access Control Camera"
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
        self.url = f"http://{self.ip_address}/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[AccessControl]"
        # self.snap_url = f"http://{self.ip_address}:{self.port}/cgi-bin/snapshot.cgi"
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
        # print('Received data: ', data)
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

                self.buffer = self.buffer[end_index:]
            else:
                break

    def process_message(self, message):
        # Find the end of the headers
        header_end_index = message.find(b"\r\n\r\n") + 4
        # Decode only the headers part to extract information
        headers = message[:header_end_index].decode("utf-8")

        # print("Headers:", headers)

        # Extract content type and content length
        content_type_match = re.search(r"Content-Type: ([\w/]+)", headers)
        content_length_match = re.search(r"Content-Length: (\d+)", headers)
        # print('Content type match: ', content_type_match)
        # print('Content length match: ', content_length_match)

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
        for content in decode_content:
            if content.startswith("Events[0].UserID="):
                temp_data["user_id"] = content.split("=")[1]
            elif content.startswith("Events[0].UTC="):
                temp_data["timestamp"] = content.split("=")[1]
        self.temp_data_storage = temp_data
        # print('Temp data storage: ', self.temp_data_storage)

    def process_image_content(self, content):
        # print('Processing image content...')
        # Check if we have already collected the necessary text data
        if self.temp_data_storage:
            # Now we have both the image and the data, send them together
            self.send_data_and_image(self.temp_data_storage, content)
            # Clear temp_data_storage after sending
            self.temp_data_storage = {}
        else:
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

    def send_data_and_image(self, data, image):
        # If cant recognize the user, return
        if "user_id" not in data:
            return
        # Generate a filename based on the event time or current time if not available
        event_time = data.get("timestamp", int(time.time()))
        filename = f"dh_ac_{event_time}"
        # with open(f"{filename}.txt", "wb") as file:
        #     file.write(json.dumps(data).encode("utf-8"))
        # Save the image content to a file
        big_img_path = self.save_temp_image(image)
        # Upload the image to Minio
        data["image_url"] = minio_services.upload_file(
            big_img_path, f"{filename}.jpg", bucket=settings.BUCKET_PLATE
        )

        to_send_data = {"id": self.process_id, "data": data}
        logger.info("Data to send: " + str(to_send_data))

        # Send the data to RabbitMQ
        self.pika_publisher.send_to_rbmq(
            data=to_send_data, exchange_name="FACE_RECOGNITION_EXCHANGES"
        )
        try:
            os.remove(big_img_path)
        except Exception:
            pass
