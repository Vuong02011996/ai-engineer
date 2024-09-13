"""Perform test request"""
import pprint
import requests

DETECTION_URL = "http://localhost:5000/v1/object-detection/yolov5"
TEST_IMAGE = "/home/gg_greenlab/Pictures/Sang.png"

image_data = open(TEST_IMAGE, "rb").read()

response = requests.post(DETECTION_URL, files={"image": image_data}).json()

pprint.pprint(response)