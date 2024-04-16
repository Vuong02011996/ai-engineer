import sys
import time
import cv2
import numpy as np
import requests
import secrets
import string
import ast
import pandas as pd

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import concurrent.futures
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt

sys.path.append("../../Convert_head_model/run_model_origin")
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import draw_boxes
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import Y5Detect
#
y5_model = Y5Detect(
    weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt")

class_names = y5_model.class_names

from shm.writer import SharedMemoryFrameWriter

# image_bgr = cv2.imread("/home/oryza/Pictures/image_test/test.png")
image_bgr = cv2.imread("/home/oryza/Pictures/image_test/img3.jpg")
# image_bgr = cv2.imread("/home/oryza/Pictures/image_test/couple.jpg")
frame_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def generate_random_key(length=24):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


session = create_session()


def test_api_model():

    process_id = "604ef817ef7c20fc5e52a20d"
    shm_w1 = SharedMemoryFrameWriter(process_id)

    start_time = time.time()

    """--------------Using Share Memory______________________"""
    # Using share memory để không phải gửi array ảnh qua payload api nặng
    shm_w1.add(frame_rgb)
    url = "http://0.0.0.0:5000/yolov5/predict/share_memory"
    # payload = {"share_key": process_id}
    # headers = {}

    data = {"share_key": process_id}

    # Send POST request to the endpoint
    response = session.post(url, json=data)
    # response = requests.post(url, json=data)

    data_out = response.json()
    data_out = ast.literal_eval(data_out)
    boxes = np.array(data_out["boxes"])
    labels = data_out["labels"]
    scores = data_out["scores"]
    detections_sort = np.array(data_out["detections_sort"])
    print("boxes: ", boxes)
    print("scores: ", scores)
    print("head_detect cost: ", time.time() - start_time)

    # image_show = draw_boxes(image_bgr, boxes, scores=scores, labels=labels, class_names=class_names)
    # cv2.namedWindow('detections', cv2.WINDOW_NORMAL)
    # cv2.imshow('detections', image_show)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # """--------------END Using Share Memory______________________"""
    return time.time() - start_time


def call_api(_):
    try:
        return test_api_model()
    except Exception as e:
        return str(e)


def test_call_100_time():
    # Number of times to call the API
    num_calls = 100

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda _: call_api(_), range(num_calls)))
        print(results)
        print(sum(results))
        # plt.plot(range(len(results)), results, marker='o', linestyle='-')
        # plt.show()
        df = pd.DataFrame(np.array(results), columns=['Values'])
        # Save DataFrame to text file
        df.to_csv(
            'model_head_' + str(num_calls) + '.txt',
            index=False)

    # Check results
    # for i, result in enumerate(results):
    #     if isinstance(result, dict):
    #         print(f"API call {i + 1} was successful.")
    #         # Process the response data if needed
    #     else:
    #         print(f"API call {i + 1} failed with error: {result}")


if __name__ == '__main__':
    test_api_model()
    # test_call_100_time()
    # session.close()