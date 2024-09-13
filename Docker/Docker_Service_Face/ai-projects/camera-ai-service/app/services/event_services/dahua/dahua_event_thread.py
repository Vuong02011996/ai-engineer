import threading
import pycurl
import logging
from app.services.event_services.dahua.dahua_base import DahuaBase

logger = logging.getLogger("event_thread")


class DahuaEventThread(threading.Thread):
    """Connects to device and subscribes to events"""

    NumActivePlayers = 0
    NumCurlObjs = 0

    def __init__(self, dahua_cfg: dict):
        """Construct a thread listening for events."""
        self.base_topic = "CameraEvents"
        self.process_id = dahua_cfg["process_id"]
        self.device: DahuaBase = dahua_cfg["device"]
        self.connected_flag = False

        CurlObj = pycurl.Curl()
        self.device.CurlObj = CurlObj
        CurlObj.setopt(pycurl.URL, self.device.url)
        CurlObj.setopt(pycurl.TCP_KEEPALIVE, 1)
        CurlObj.setopt(pycurl.TCP_KEEPIDLE, 30)
        CurlObj.setopt(pycurl.TCP_KEEPINTVL, 15)
        CurlObj.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_DIGEST)
        CurlObj.setopt(
            pycurl.USERPWD, "%s:%s" % (self.device.username, self.device.password)
        )
        # CurlObj.setopt(pycurl.WRITEFUNCTION, self.device.OnReceive)

        self.CurlObj = CurlObj

        print("Added Dahua device at: %s", self.device.url)
        threading.Thread.__init__(
            self, daemon=True
        )  # IMPORTANT: when the main thread exits, this thread will also exit
        self.stopped = threading.Event()
        self.should_stop = False

    def run(self):
        print("Started DahuaEventThread")
        self.CurlObj.setopt(pycurl.WRITEFUNCTION, self.write_function)
        while not self.stopped.is_set():
            try:
                self.CurlObj.perform()
            except pycurl.error as e:
                print(f"Error occurred: {e}")
                break
        print("Exiting run method")

    def write_function(self, data):
        if self.should_stop:
            raise pycurl.error("Forced stop error")
        self.device.OnReceive(data)
        return len(data)

    def stop(self):
        self.should_stop = True
        self.stopped.set()
        print("Stopped DahuaEventThread")
