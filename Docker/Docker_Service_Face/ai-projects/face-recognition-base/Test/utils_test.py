import traceback
import uuid
import secrets
import string
from datetime import datetime
import requests
import cv2
import io
import numpy as np
from io import BytesIO
from PIL import Image
import os
import time
import pyheif
from sentry_sdk import capture_message

ip_run_service_ai = os.getenv("ip_run_service_ai")

def random_uuid():
    # Generate a UUID
    random_key = uuid.uuid4()

    # Convert UUID to string
    random_key_str = str(random_key)

    print(random_key_str)


def generate_random_key(length=24):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def read_arr_image_from_url(url):
    try:
        img = io.imread(url)
    except Exception as e:
        print("Lỗi đọc ảnh từ url: ", e)
        img = None
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
    return img


def read_url_img_to_array(url):
    if url[-4:] == "HEIC":
        response = requests.get(url)
        bytesIo = response.content
        i = pyheif.read(bytesIo)
        pi = Image.frombytes(
            mode=i.mode, size=i.size, data=i.data)
        img = np.array(pi)
        """Không cần resize vì qua model đã resize(1000, 1000)"""


    # https://pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
    else:
        try:
            img = io.imread(url)
        except Exception as e:
            print("Lỗi đọc ảnh từ url: ", e)
            img = None
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
    return img


if __name__ == '__main__':

    # random_key = generate_random_key()
    # print(random_key)

    # print("time now: ", str(datetime.utcnow()))
    # url = "https://erp-tuan.oryza.vn/web/image/401-5657b1a9/Vinh.jpg"
    # url = "https://erp-tuan.oryza.vn/web/image/398-5657b1a9/Vinh.jpg"
    # url = "https://erp-tuan.oryza.vn/web/image/79-877806ee/photo_2024-03-15_14-33-47.jpg"
    url = "https://erp-tuan.oryza.vn/web/image/100-cf926580/L%C3%AA%20Th%E1%BB%8B%20H%E1%BB%93ng%20Th%E1%BA%A3o.jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = np.array(img)
    # cv2.imwrite("test.jpg", img)
    # print(img.shape)
    # read_url_img_to_array(url)