import os
import json
import base64
import requests
import glob
import cv2
import concurrent.futures


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
    image = cv2.imread("/home/oryza/Pictures/image_test/couple.jpg")
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


def face_detection():
    image = cv2.imread("/home/oryza/Pictures/image_test/couple.jpg")
    image_base64 = convert_np_array_to_base64(image)
    req = {
        "images": {
            "data": [image_base64],
        },
    }
    resp = requests.post('http://localhost:18081/extract', json=req)
    data = resp.json()
    return data


def call_api():
    try:
        return face_detection()
    except Exception as e:
        return str(e)


def check_call_many_times_at_the_same_time():
    # Number of times to call the API
    num_calls = 100

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(call_api, range(num_calls)))

    # Check results
    for i, result in enumerate(results):
        if isinstance(result, dict):
            print(f"API call {i + 1} was successful.")
            # Process the response data if needed
        else:
            print(f"API call {i + 1} failed with error: {result}")


if __name__ == '__main__':
    images_path = '/home/oryza/Pictures/image_test'
    # images = os.path.listdir(images_path)
    images = glob.glob(os.path.join(images_path, '*.jpg'))
    data = extract_vecs(images)

    # test_array_image()
