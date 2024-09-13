import socket
import paho.mqtt.client as paho
import logging


logger = logging.getLogger("paho_client")


class PahoClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = paho.Client(
                "CameraEvents-" + socket.gethostname(), clean_session=True
            )
            cls._instance.connected_flag = False  # Initialize connected_flag
            logger.debug("Connecting to MQTT Broker")
            cls._instance.connect("localhost", 1883, 60)
            logger.debug("Starting MQTT Loop")
            cls._instance.loop_start()
        return cls._instance


paho_client = PahoClient()
