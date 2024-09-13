import os
import re
import logging
import time
from app.services.pika_publisher import pika_publisher

logger = logging.getLogger("dahua")


class DahuaBase:
    def __init__(self, config: dict):
        self.name = ""
        self.code = ""
        self.rbmq_exchange = ""

        # Setting from request
        self.username = config["username"]
        self.password = config["password"]
        self.address = config["ip_address"]
        self.port = config["port"]
        self.process_id = config["process_id"]
        # Dahua Camera default settings
        self.channel = 1
        self.auth = "digest"
        self.protocol = "http"
        self.alerts = True
        self.basetopic = "CameraEvents"
        self.isNVR = True

        # Dahua Camera connection settings
        self.CurlObj = None
        self.Connected = None
        self.Reconnect = None
        self.MQTTConnected = None

        # For parsing the incoming data
        self.buffer = b""
        self.boundary = b"--myboundary"
        self.url = ""  # Initialize URL
        self.expected_length = None

    def construct_url(self):
        self.url = f"http://{self.address}:{self.port}/cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events={self.code}"
        print(self.url)

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
        # print('OnReceive')
        self.buffer += data
        while True:
            start_index = self.buffer.find(self.boundary)
            if start_index == -1:
                # No start boundary found, exit loop to wait for more data
                break
            end_index = self.buffer.find(
                self.boundary, start_index + len(self.boundary)
            )
            if end_index == -1:
                # End boundary not found, check if we can extract content length
                header_end_index = self.buffer.find(b"\r\n\r\n") + 4
                if header_end_index > 4:
                    headers = self.buffer[:header_end_index].decode("utf-8")
                    content_length_match = re.search(r"Content-Length: (\d+)", headers)
                    if content_length_match:
                        content_length = int(content_length_match.group(1))
                        if len(self.buffer) >= header_end_index + content_length:
                            # We have a complete message based on content length
                            message = self.buffer[: header_end_index + content_length]
                            self.process_message(message)
                            self.buffer = self.buffer[
                                header_end_index + content_length :
                            ]
                            continue
                # If we reach here, we don't have enough data to process; break to wait for more
                break

            # If end boundary is found, process as before
            message = self.buffer[start_index:end_index]
            self.process_message(message)
            self.buffer = self.buffer[end_index:]

    def process_message(self, message):
        header_end_index = message.find(b"\r\n\r\n") + 4
        headers = message[:header_end_index].decode("utf-8")
        content_type_match = re.search(r"Content-Type: ([\w/]+)", headers)
        content_length_match = re.search(r"Content-Length: (\d+)", headers)
        if content_type_match and content_length_match:
            content_type = content_type_match.group(1)
            content_length = int(content_length_match.group(1))
            actual_content = message[
                header_end_index : header_end_index + content_length
            ]
            if content_type == "text/plain":
                self.process_text_content(actual_content)
            elif content_type == "image/jpeg":
                self.process_image_content(actual_content)

    def custom_decode(self, content: dict):
        return {}

    def process_text_content(self, content):
        decode_content = content.decode("utf-8")
        decode_content = decode_content.split("\r\n")
        decode_content.pop()
        content_json = self.parse_event_data(decode_content)
        self.temp_data_storage = self.custom_decode(content_json)

    def process_image_content(self, content):
        # Check if we have already collected the necessary text data
        if self.temp_data_storage:
            # Now we have both the image and the data, send them together
            self.send_data_and_image(self.temp_data_storage, content)
            # Clear temp_data_storage after sending
            self.temp_data_storage = {}
        # else:
        # If we don't have the text data yet, just store the image temporarily
        # logger.info(
        #     "Received image without preceding text data. Image disregarded."
        # )

    def save_temp_image(self, content, temp_name=None):
        import random
        import string

        if temp_name is None:
            temp_name = f"{int(time.time())}"
        rand_id = f"{random.randint(100, 999)}{random.choice(string.ascii_letters)}"
        temp_name = f"{temp_name}_{rand_id}.jpg"
        try:
            path = os.path.join("./temp", temp_name)
            if not os.path.exists("./temp"):
                os.makedirs("./temp")
            with open(path, "wb") as f:
                f.write(content)
            return temp_name, path
        except Exception as e:
            logger.error(f"Error saving image content: {e}")
            return False, False

    def custom_data_to_send(self, data: dict, image):
        return {}

    def send_data_and_image(self, data: dict, image):
        # If cant recognize the user, return
        data = self.custom_data_to_send(data, image)
        if not data:
            return
        data["camera_ip"] = self.address
        try:
            data["timestamp"] = int(data["timestamp"])
        except Exception:
            data["timestamp"] = int(time.time())
        to_send_data = {
            "id": self.process_id,
            "data": data,
        }
        logger.info("Data to send: " + str(to_send_data))

        # Send the data to RabbitMQ
        pika_publisher.send_to_rbmq(data=to_send_data, exchange_name=self.rbmq_exchange)

    def parse_event_data(self, decode_content: list):
        def deep_set(dic, keys, value):
            for i, key in enumerate(keys[:-1]):
                if isinstance(key, int):
                    while isinstance(dic, dict) and key not in dic:
                        dic[key] = []
                    if isinstance(dic, list):
                        while len(dic) <= key:
                            dic.append({})
                    dic = dic[key]
                else:
                    if key not in dic:
                        next_key = keys[i + 1]
                        dic[key] = [] if isinstance(next_key, int) else {}
                    dic = dic[key]

            if isinstance(keys[-1], int):
                if not isinstance(dic, list):
                    dic[keys[-1]] = []
                while len(dic) <= keys[-1]:
                    dic.append(None)
                dic[keys[-1]] = value
            else:
                dic[keys[-1]] = value

        def parse_key(key):
            parts = re.split(r"\.|\[|\]", key)
            keys = [int(part) if part.isdigit() else part for part in parts if part]
            return keys

        def decode_to_json(decode_content: list):
            result = {}
            for content in decode_content:
                key, value = content.split("=")
                keys = parse_key(key)
                deep_set(result, keys, value)
            result = result.get("Events", [{}])[0]
            return result

        return decode_to_json(decode_content)
