import threading
import pycurl
import socket
import paho.mqtt.client as paho
import time
import datetime
import logging
import select

from old_code.access_control import AccessControl

EVENT_THREAD_LOGGER = logging.getLogger("ac_event_thread")


class PahoClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = paho.Client(
                "CameraEvents-" + socket.gethostname(), clean_session=True
            )
            cls._instance.connected_flag = False  # Initialize connected_flag
            EVENT_THREAD_LOGGER.debug("Connecting to MQTT Broker")
            cls._instance.connect("localhost", 1883, 60)
            EVENT_THREAD_LOGGER.debug("Starting MQTT Loop")
            cls._instance.loop_start()
        return cls._instance


class DahuaAccessControlThread(threading.Thread):
    """Connects to device and subscribes to events"""

    NumActivePlayers = 0
    NumCurlObjs = 0

    def __init__(self, dahua_cfg: dict):
        """Construct a thread listening for events."""
        self.base_topic = "CameraEvents"
        self.process_id = dahua_cfg["process_id"]
        self.client = PahoClient()
        device = AccessControl(client=self.client, config=dahua_cfg)
        self.device = device

        self.client.on_connect = self.mqtt_on_connect
        self.client.on_disconnect = self.mqtt_on_disconnect
        self.CurlMultiObj = pycurl.CurlMulti()
        self.CurlObj = pycurl.Curl()
        device.CurlObj = self.CurlObj
        self.CurlObj.setopt(pycurl.URL, device.url)
        self.CurlObj.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.CurlObj.setopt(pycurl.TCP_KEEPALIVE, 1)
        self.CurlObj.setopt(pycurl.TCP_KEEPIDLE, 30)
        self.CurlObj.setopt(pycurl.TCP_KEEPINTVL, 15)

        self.CurlObj.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
        self.CurlObj.setopt(
            pycurl.USERPWD, "%s:%s" % (device.username, device.password)
        )

        self.CurlMultiObj.add_handle(self.CurlObj)
        self.NumCurlObjs += 1

        EVENT_THREAD_LOGGER.debug("Added AC Dahua device at: %s", device.url)

        threading.Thread.__init__(
            self, daemon=True
        )  # IMPORTANT: when the main thread exits, this thread will also exit
        self.stopped = threading.Event()

    def run(self):
        EVENT_THREAD_LOGGER.info("Started ACDahuaBTEventThread")
        heartbeat = 0
        """Fetch events"""
        while not self.stopped.is_set():
            # Sleeps to ease load on processor
            time.sleep(0.05)
            heartbeat = heartbeat + 1
            if heartbeat % 1000 == 0:
                EVENT_THREAD_LOGGER.debug("Heartbeat: " + str(datetime.datetime.now()))
                if not self.client.connected_flag:
                    self.client.reconnect()
                self.client.publish(
                    self.base_topic + "/$heartbeat", str(datetime.datetime.now())
                )

            # Wait for activity on the curl object with a timeout
            while True:
                ret, num_handles = self.CurlMultiObj.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break

            # Set the write function
            self.CurlObj.setopt(pycurl.WRITEFUNCTION, self.device.OnReceive)

            # Wait for activity on the curl object with a timeout
            while True:
                ret, num_handles = self.CurlMultiObj.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break

            # If there's no more data to process at the moment
            if num_handles == 0:
                break
            rlist, wlist, xlist = self.CurlMultiObj.fdset()
            select.select(rlist, wlist, xlist, 1)

    def stop(self):
        self.stopped.set()
        self.client.loop_stop()  # Stop the MQTT loop
        self.client.disconnect()  # Disconnect the MQTT client
        self.CurlObj.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        EVENT_THREAD_LOGGER.info("Stopped DahuaBTEventThread")

    def mqtt_on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            EVENT_THREAD_LOGGER.info(
                "Connected to MQTT OK Returned code = {0}".format(rc)
            )
            self.client.connected_flag = True
        else:
            EVENT_THREAD_LOGGER.info(
                "Camera : {0}: Bad mqtt connection Returned code = {1}".format(
                    "self.Name", rc
                )
            )
            self.client.connected_flag = False

    def mqtt_on_disconnect(self, client, userdata, rc):
        EVENT_THREAD_LOGGER.info("disconnecting reason  " + str(rc))
        self.client.connected_flag = False
        if rc != 0:
            # Unexpected disconnection
            while not self.client.connected_flag:  # Try to reconnect until successful
                try:
                    self.client.reconnect()
                except Exception:
                    pass
                time.sleep(1)  # Wait a bit before trying again
