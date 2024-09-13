import os
import json
import base64
import requests
import glob
import time


def file2base64(path):
    with open(path, mode='rb') as fl:
        encoded = base64.b64encode(fl.read()).decode('ascii')
        return encoded


def extract_vecs(ims, max_size=[640, 480]):
    target = [file2base64(im) for im in ims]
    req = {"images": {"data": target}, "max_size": max_size}
    # resp = requests.post('http://localhost:18081/extract', json=req)
    # resp = requests.post('http://192.168.111.98:18081/extract', json=req)
    # resp = requests.post('http://192.168.111.11:18081/extract', json=req)
    resp = requests.post("http://api-face.oryza.vn" + '/extract', json=req)
    data = resp.json()
    return data


if __name__ == '__main__':
    images_path = '/home/oryza/Pictures/image_test'
    # images = os.path.listdir(images_path)
    images = glob.glob(os.path.join(images_path, '*.jpg'))
    # images_path = 'src/api/test_images'
    # images = os.path.listdir(images_path)
    start_time = time.time()
    data = extract_vecs(images[:3])
    print("Cost: ", time.time() - start_time)
    # print("data: ", data)