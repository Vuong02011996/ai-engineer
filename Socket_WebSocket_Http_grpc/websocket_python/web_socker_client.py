import asyncio
import sys
import time
import cv2
import numpy as np
import requests
import secrets
import string
import ast
import pandas as pd
from websockets.sync.client import connect
from shm.writer import SharedMemoryFrameWriter


image_bgr = cv2.imread("/home/oryza/Pictures/image_test/test.png")
frame_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def hello():
    with connect("ws://localhost:8765") as websocket:
        # share image data with sharememory
        process_id = "604ef817ef7c20fc5e52a20d"
        shm_w1 = SharedMemoryFrameWriter(process_id)
        shm_w1.add(frame_rgb)

        # send share_key for server
        websocket.send(process_id)
        message = websocket.recv()
        print(f"Received: {message}")


hello()