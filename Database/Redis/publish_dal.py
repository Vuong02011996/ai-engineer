import os
import redis
import time
import json
from threading import Thread


"""
REDIS_HOST="14.224.128.168"
REDIS_PORT=63799
REDIS_PASSWORD="Q2xvdmVyQDEyMw=="
REDIS_DB=0
CHANNEL_GROUPING="image_grouping"
CHANNEL_REGISTER="register_channel"
"""

if os.getenv("REDIS_PASSWORD") is None:
    redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)
else:
    redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0,
                                     password=os.getenv("REDIS_PASSWORD"))


class Pusher:
    def __init__(self) -> None:
        self._start = None
        self._end = None
        self._interval = 1

    def set_interval(self, interval):
        self._interval = interval

    def start(self):
        if self._start is None:
            self._start = time.time()

    def stop(self):
        raise NotImplementedError()

    def get_interval(self):
        current_time = time.time()
        if self._start:
            return current_time - self._start
        raise None

    @staticmethod
    def publish_thread(channel, data):
        redis_client.publish(channel, json.dumps(data))

    def publish(self, channel, data, is_directly=False):
        """ Directly publish the data to redis pub/sub or by time interval """
        if is_directly:
            t = Thread(target=self.publish_thread, args=[channel, data])
            t.start()
        else:
            try:
                if self.get_interval() >= self._interval:
                    self._start = time.time()
                    redis_client.publish(channel, json.dumps(data))
            except Exception as error:
                print("error:", error)