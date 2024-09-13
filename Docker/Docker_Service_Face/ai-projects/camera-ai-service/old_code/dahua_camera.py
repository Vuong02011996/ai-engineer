import json
import logging
from datetime import datetime
from app.services.dahua_find_media_services import DahuaFindMediaService
from app.services.pika_publisher import pika_publisher
from app.common.utils import get_times_around_event

logger = logging.getLogger("dahua_bt_logger")


class DahuaCamera:
    def __init__(self, config: dict):
        # Setting from request
        self.name = "Face Recognition Camera"
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
        self.url = f"http://{self.ip_address}:{self.port}/cgi-bin/eventManager.cgi?action=attach&codes=%5BFaceRecognition%5D"
        self.isNVR = True

        # DahuaBT Camera connection settings
        self.CurlObj = None
        self.Connected = None
        self.Reconnect = None
        self.MQTTConnected = None

        # DahuaBT Camera settings
        self.find_media_services = DahuaFindMediaService(
            server=self.ip_address, username=self.username, password=self.password
        )
        self.pika_publisher = pika_publisher

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
        event_time = datetime.now()
        logger.info(f"Event time: {event_time}")
        # Parse the data
        logger.info("OnReceive function called...")
        decoded_data = data.decode("utf-8", errors="ignore")
        # print("Decoded data: ", decoded_data)
        # print("-----------------------------------------------------")
        for part in decoded_data.split("\r\n"):
            if part == "HTTP/1.1 200 OK":
                self.OnConnect()
            if not part.startswith("Code=FaceRecognition;action=Start;index=0;data="):
                continue

            # Got the right part -> start processing data
            logger.info("Event time: %s", str(event_time))
            part = part.replace("Code=FaceRecognition;action=Start;index=0;data=", "")
            # logger.info("Data received: " + part)
            try:
                logger.info("Data received -> parsing... ")
                data_dict = json.loads(part)
                if "Candidates" not in data_dict or not data_dict["Candidates"]:
                    logger.debug("Cant recognize")
                    continue
            except json.decoder.JSONDecodeError:
                logger.debug("Invalid JSON string: " + part)
                continue

            # Send the data to RabbitMQ
            id = data_dict["Candidates"][0]["Person"]["ID"]
            certificate_type = data_dict["Candidates"][0]["Person"]["CertificateType"]

            # Try to get the image, if not found, try to get the image in the next 5 seconds
            delta_seconds = 0
            while delta_seconds < 5:
                start_time, end_time = get_times_around_event(
                    event_time=event_time, delta_seconds=delta_seconds
                )
                condition = {
                    "Channel": 1,
                    "StartTime": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "EndTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Types": ["jpg"],
                    "Flags": ["Event"],
                    "Events": ["FaceRecognition"],
                    "ID": id,
                    "certificate_type": certificate_type,
                }
                logger.info("Condition: " + str(condition))
                timestamp, image_url = self.find_media_services.get_image_url(
                    condition=condition
                )
                if timestamp is not None and image_url is not None:
                    break
                delta_seconds += 1
                if delta_seconds == 5:
                    logger.debug("No image found")
                    return

            to_send_data = {
                "id": self.process_id,
                "data": {
                    "user_id": data_dict["Candidates"][0]["Person"]["UID"],
                    "timestamp": int(timestamp.timestamp()),
                    "camera_ip": self.ip_address,
                    "image_url": image_url,
                },
            }
            logger.info("Data to send: " + str(to_send_data))

            # Send the data to RabbitMQ
            self.pika_publisher.send_to_rbmq(
                data=to_send_data, exchange_name="FACE_RECOGNITION_EXCHANGES"
            )
