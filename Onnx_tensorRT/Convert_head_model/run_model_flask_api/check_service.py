import sys
import time
import cv2
import numpy as np
import requests
import secrets
import string

sys.path.append("../../Convert_head_model/run_model_origin")
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import draw_boxes
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import Y5Detect
#
y5_model = Y5Detect(
    weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt")

class_names = y5_model.class_names

from shm.writer import SharedMemoryFrameWriter


def generate_random_key(length=24):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def head_detect(cam, frame_detect_queue, detections_queue):
    process_id = "604ef817ef7c20fc5e52a20d"
    shm_w1 = SharedMemoryFrameWriter(process_id)
    while cam.cap.isOpened():
        frame_rgb, frame_count = frame_detect_queue.get()
        start_time = time.time()
        #
        # boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["head"])
        # print("head_detect cost: ", time.time() - start_time)

        """--------------Using Share Memory______________________"""
        shm_w1.add(frame_rgb)
        url = "http://0.0.0.0:5000/yolov5/predict/share_memory"
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload)
        data_out = response.json()
        boxes = np.array(data_out["boxes"])
        labels = data_out["labels"]
        scores = data_out["scores"]
        detections_sort = np.array(data_out["detections_sort"])
        print("head_detect cost: ", time.time() - start_time)
        """--------------END Using Share Memory______________________"""

        detections_queue.put([boxes, labels, scores, frame_rgb, detections_sort, frame_count])

    cam.cap.release()


def test_api_model(frame_rgb):
    process_id = "604ef817ef7c20fc5e52a20d"
    shm_w1 = SharedMemoryFrameWriter(process_id)

    start_time = time.time()
    #
    # boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["head"])
    # print("head_detect cost: ", time.time() - start_time)

    """--------------Using Share Memory______________________"""
    # Using share memory để không phải gửi array ảnh qua payload api nặng
    shm_w1.add(frame_rgb)
    url = "http://0.0.0.0:5000/yolov5/predict/share_memory"
    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data_out = response.json()
    boxes = np.array(data_out["boxes"])
    labels = data_out["labels"]
    scores = data_out["scores"]
    detections_sort = np.array(data_out["detections_sort"])
    print("head_detect cost: ", time.time() - start_time)
    image_show = draw_boxes(image_bgr, boxes, scores=scores, labels=labels, class_names=class_names)
    cv2.namedWindow('detections', cv2.WINDOW_NORMAL)
    cv2.imshow('detections', image_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """--------------END Using Share Memory______________________"""


def head_detect_service(cam, frame_detect_queue, detections_queue):
    # process_id = "604ef817ef7c20fc5e52a20d"
    process_id = generate_random_key()
    shm_w1 = SharedMemoryFrameWriter(process_id)
    while cam.cap.isOpened():
        frame_rgb, frame_count = frame_detect_queue.get()
        start_time = time.time()
        # boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["head"])
        # print("head_detect cost: ", time.time() - start_time)

        # data = nparray_to_bytebuffer(frame_rgb)
        # headers = {'Content-Type': 'image/jpeg'}

        # Using shm

        shm_w1.add(frame_rgb)
        url = "http://0.0.0.0:5000/yolov5/predict/share_memory"
        payload = {"share_key": process_id}
        headers = {}

        response = requests.post(url, headers=headers, data=payload)
        response = response.json()
        boxes = np.array(response["boxes"]).astype(int)
        labels = np.array(response["labels"])
        scores = np.array(response["scores"])
        detections_sort = np.array(response["detections_sort"])
        print("head_detect cost: ", time.time() - start_time)
        print("boxes, labels, scores, detections_sort: ", boxes, labels, scores, detections_sort)

        detections_queue.put([boxes, labels, scores, frame_rgb, detections_sort, frame_count])

    cam.cap.release()


if __name__ == '__main__':
    image_bgr = cv2.imread("/home/oryza/Pictures/image_test/test.png")
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    test_api_model(image_rgb)