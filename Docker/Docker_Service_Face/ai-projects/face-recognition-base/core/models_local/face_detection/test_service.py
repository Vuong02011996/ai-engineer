import os
import json
import base64
import requests
import glob
import cv2

from core.main.main_utils.helper import convert_np_array_to_base64


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
    url_face = "http://localhost:18081/extract"
    image1 = cv2.imread("/home/oryza/Pictures/image_test/couple.jpg")
    image2 = cv2.imread("/home/oryza/Pictures/image_test/img11.jpg")  # prob: 0.714
    image3 = cv2.imread("/home/oryza/Pictures/image_test/Khoi.jpg")  # 0.7995
    image_base64_1 = convert_np_array_to_base64(image1)
    image_base64_2 = convert_np_array_to_base64(image2)
    image_base64_3 = convert_np_array_to_base64(image3)
    list_image = []
    list_image.append(image_base64_2)
    # list_image.append(image_base64_3)
    req = {
        "images": {
            # "data": [
            #     "string"
            # ],
            "data": list_image,
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
    # resp = requests.post('http://localhost:18081/extract', json=req)

    req = {"images": {"data": list_image}, "threshold": 0.65, "return_landmarks": True, "embed_only": False,
           "extract_embedding": False}
    resp = requests.post(url_face, json=req)

    data = resp.json()
    return data


if __name__ == '__main__':
    # images_path = '/home/oryza/Pictures/image_test'
    # # images = os.path.listdir(images_path)
    # images = glob.glob(os.path.join(images_path, '*.jpg'))
    # data = extract_vecs(images)

    test_array_image()
