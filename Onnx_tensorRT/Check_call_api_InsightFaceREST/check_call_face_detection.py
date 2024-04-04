import os
import json
import base64
import requests
import glob
import cv2
import concurrent.futures
import time
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt


path_test_batch = "/home/oryza/Pictures/image_head_test_batch_size/"
url_face = 'http://localhost:18081/extract'


def convert_np_array_to_base64(image):
    """

    :param image: np array image
    :return: string image base64
    """
    success, encoded_image = cv2.imencode('.jpg', image)
    image_face = encoded_image.tobytes()
    image_base64 = base64.b64encode(image_face).decode('ascii')
    return image_base64


def file2base64(path):
    with open(path, mode='rb') as fl:
        encoded = base64.b64encode(fl.read()).decode('ascii')
        return encoded


def extract_vecs(ims, max_size=[640, 480]):
    target = [file2base64(im) for im in ims]
    # req = {"images": {"data": target},"max_size":max_size}
    # resp = requests.post('http://localhost:18081/extract', json=req)

    # req = {"images": {"data": target}, "threshold": 0.65, "return_landmarks": True, "embed_only": False,
    #        "extract_embedding": False}
    req = {
        "images": {
            # "data": [
            #     "string"
            # ],
            "data": target,
            # "urls": [
            #     "/home/oryza/Pictures/image_test/couple.jpg"
            # ]
        },
        # "max_size": [
        #     640,
        #     640
        # ],
        # "threshold": 0.6,
    }
    # start_time = time.time()
    resp = requests.post('http://localhost:18081/extract', json=req)
    data = resp.json()
    return data


def test_array_image():
    image = cv2.imread(path_test_batch + "head_4_5.png")
    image_base64 = convert_np_array_to_base64(image)
    req = {
        "images": {
            # "data": [
            #     "string"
            # ],
            "data": [image_base64],
            # "urls": [
            #     "/home/oryza/Pictures/image_test/couple.jpg"
            # ]
        },
        # "max_size": [
        #     640,
        #     640
        # ],
        # "threshold": 0.6,
    }
    # start_time = time.time()
    resp = requests.post('http://localhost:18081/extract', json=req)
    data = resp.json()
    return data


def face_detection_batch():
    # image = cv2.imread(path_test_batch + "head_4_5.png")
    images = glob.glob(os.path.join(path_test_batch, '*.png'))
    print("len(images): ", len(images))
    target = []
    for img in images[:5]:
        img = cv2.imread(img)
        image_base64 = convert_np_array_to_base64(img)
        target.append(image_base64)

    req = {"images": {"data": target}, "threshold": 0.5, "return_landmarks": True, "embed_only": False,
           "extract_embedding": False}
    start_time = time.time()
    resp = requests.post(url_face, json=req)
    data = resp.json()
    # print(data)
    print("cost: ", time.time() - start_time)
    return time.time() - start_time


def face_detection():
    image = cv2.imread(path_test_batch + "head_4_5.png")
    image_base64 = convert_np_array_to_base64(image)
    start_time = time.time()
    req = {
        "images": {
            "data": [image_base64],
        },
    }
    resp = requests.post('http://localhost:18081/extract', json=req)
    data = resp.json()
    # print(data)
    print("cost ", time.time() - start_time)
    return time.time() - start_time


def call_api(_):
    try:
        # return face_detection()
        return face_detection_batch()
    except Exception as e:
        return str(e)


def check_call_many_times_at_the_same_time():
    # Number of times to call the API
    num_calls = 10000

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda _: call_api(_), range(num_calls)))
        print(results)
        print(sum(results))
        plt.plot(range(len(results)), results, marker='o', linestyle='-')
        plt.show()


if __name__ == '__main__':
    # images_path = '/home/oryza/Pictures/image_test'
    # # images = os.path.listdir(images_path)
    # images = glob.glob(os.path.join(images_path, '*.jpg'))
    # data = extract_vecs(images)

    # test_array_image()
    check_call_many_times_at_the_same_time()
