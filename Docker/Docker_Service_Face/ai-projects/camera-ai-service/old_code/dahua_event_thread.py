import threading
import pycurl
import time
import random
import datetime
import logging
import socket
import paho.mqtt.client as paho
from app.services.event_services.dahua.dahua_base import DahuaBase

logger = logging.getLogger("event_thread")


class DahuaEventThread(threading.Thread):
    """Connects to device and subscribes to events"""

    Devices = []
    NumActivePlayers = 0
    CurlMultiObj = pycurl.CurlMulti()
    NumCurlObjs = 0

    def __init__(self, cameras):
        # mqtt
        mqtt = {"IP": "localhost", "port": 1883}

        """Construct a thread listening for events."""
        self.basetopic = "CameraEvents"
        self.homebridge = "homebridge"
        self.process_id = cameras[0].get("process_id")
        self.client = paho.Client(
            f"CameraEvents-{socket.gethostname()}-{random.randint(1, 1000)}",
            clean_session=True,
        )
        self.client.on_connect = self.mqtt_on_connect
        self.client.on_disconnect = self.mqtt_on_disconnect
        self.client.will_set(self.basetopic + "/$online", False, qos=0, retain=True)

        for device_cfg in cameras:
            device: DahuaBase = device_cfg["device"]
            logger.info(
                f"Device {device.name} created on url {device.url}. Alert: {device.alerts}"
            )
            self.Devices.append(device)

            CurlObj = pycurl.Curl()
            device.CurlObj = CurlObj

            CurlObj.setopt(pycurl.URL, device.url)
            CurlObj.setopt(pycurl.CONNECTTIMEOUT, 30)
            CurlObj.setopt(pycurl.TCP_KEEPALIVE, 1)
            CurlObj.setopt(pycurl.TCP_KEEPIDLE, 30)
            CurlObj.setopt(pycurl.TCP_KEEPINTVL, 15)
            if device.auth == "digest":
                CurlObj.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
                CurlObj.setopt(
                    pycurl.USERPWD, "%s:%s" % (device.username, device.password)
                )
            else:
                CurlObj.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH)
                CurlObj.setopt(
                    pycurl.USERPWD, "%s:%s" % (device.username, device.password)
                )
            CurlObj.setopt(pycurl.WRITEFUNCTION, device.OnReceive)

            self.CurlMultiObj.add_handle(CurlObj)
            self.NumCurlObjs += 1

            logger.debug("Added Dahua device at: {device.url}")

        logger.debug("Connecting to MQTT Broker")
        self.client.connect(mqtt["IP"], mqtt["port"], 60)

        logger.debug("Starting MQTT Loop")
        self.client.loop_start()

        threading.Thread.__init__(
            self, daemon=True
        )  # IMPORTANT: when the main thread exits, this thread will also exit
        self.stopped = threading.Event()

    def run(self):
        logger.info("Started DahuaEventThread")
        heartbeat = 0
        while True:
            Ret, NumHandles = self.CurlMultiObj.perform()
            if Ret != pycurl.E_CALL_MULTI_PERFORM:
                break

        Ret = self.CurlMultiObj.select(1.0)
        while not self.stopped.is_set():
            # Sleeps to ease load on processor
            time.sleep(0.05)  # Sleeps to ease load on processor
            heartbeat += 1
            if heartbeat % 1000 == 0:
                logger.debug("Heartbeat: %s", datetime.datetime.now())
                if not self.client.connected_flag:
                    self.client.reconnect()
                self.client.publish(
                    self.basetopic + "/$heartbeat", str(datetime.datetime.now())
                )

            Ret, NumHandles = self.CurlMultiObj.perform()

            if NumHandles != self.NumCurlObjs:
                _, Success, Error = self.CurlMultiObj.info_read()

                for CurlObj in Success:
                    DahuaDevice: DahuaBase = next(
                        iter(filter(lambda x: x.CurlObj == CurlObj, self.Devices)), None
                    )
                    if DahuaDevice.Reconnect:
                        logger.debug(f"Dahua Reconnect: {DahuaDevice.Name}")
                        continue

                    DahuaDevice.OnDisconnect("Success")
                    DahuaDevice.Reconnect = time.time() + 5

                for CurlObj, ErrorNo, ErrorStr in Error:
                    DahuaDevice = next(
                        iter(filter(lambda x: x.CurlObj == CurlObj, self.Devices)), None
                    )
                    if DahuaDevice.Reconnect:
                        continue

                    DahuaDevice.OnDisconnect(f"{ErrorStr} ({ErrorNo})")
                    DahuaDevice.Reconnect = time.time() + 5

                for DahuaDevice in self.Devices:
                    if DahuaDevice.Reconnect and DahuaDevice.Reconnect < time.time():
                        self.CurlMultiObj.remove_handle(DahuaDevice.CurlObj)
                        self.CurlMultiObj.add_handle(DahuaDevice.CurlObj)
                        DahuaDevice.Reconnect = None

    def stop(self):
        self.stopped.set()
        self.join()
        self.client.disconnect()

    def mqtt_on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT OK Returned code = {rc}")
            self.client.connected_flag = True
        else:
            logger.info(f"Camera {self.Name}: Bad mqtt connection Returned code = {rc}")
            self.client.connected_flag = False

    def mqtt_on_disconnect(self, client, userdata, rc):
        logger.info("disconnecting reason  " + str(rc))
        self.client.connected_flag = False
