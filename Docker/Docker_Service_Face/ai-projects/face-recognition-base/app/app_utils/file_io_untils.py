import traceback
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

import connect_db # Thêm dòng này mới load được biến môi trường ở đây.



"""
Note: 
+ swagger : https://erp-clover-file.demo.greenglobal.com.vn/swagger/index.html
+ Upload video
+ Upload array image
"""

# path_save_local = os.getenv("path_save_local")


url_api_save_file = os.getenv("url_api_save_file")
url_server_save_file = os.getenv("url_server_save_file")
ip_run_service_ai = os.getenv("ip_run_service_ai")



# path_save_local = "/DATA/data/DATA/Clover_data/Image_URL/"


def upload_img_from_disk(image_name=None, img_arr=None):
    # img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    file_buffer = io.BytesIO()
    file_buffer.write(cv2.imencode('.png', img_arr)[1])
    file_buffer.seek(0)
    data = {'files': ('image.png', file_buffer)}

    # file_name = path_save_local + image_name + ".png"
    # cv2.imwrite(file_name, img_arr)
    # data = {'files': open(file_name, 'rb')}

    start_time_url_api_save_file = time.time()
    result = requests.post(url_api_save_file, files=data)
    print("upload_img_from_disk cost: ", time.time() - start_time_url_api_save_file)
    url_output = None
    if result.status_code >= 500:
        print("Server url_api_save_file error occurred. Status code:", result.status_code, result.reason)
    elif result.status_code >= 400:
        print("Client  url_api_save_file error occurred. Status code:", result.status_code, result.reason)
    else:
        print("Request successful. Status code:", result.status_code)
        url_output = url_server_save_file + result.json()["results"][0]["fileInfo"]["url"]
    return url_output


def get_url_from_array_image_to_file_server(img_arr):
    file_buffer = io.BytesIO()
    file_buffer.write(cv2.imencode('.png', img_arr)[1])
    file_buffer.seek(0)
    data = {'files': ('image.png', file_buffer)}
    result = requests.post(url_api_save_file, files=data)
    url_output = url_server_save_file + result.json()["results"][0]["fileInfo"]["url"]
    return url_output


def upload_video_from_disk_server_and_get_link(file_name):
    data = {'files': open(file_name, 'rb')}
    url = requests.post(url_api_save_file, files=data)
    url_output = url_server_save_file + url.json()["results"][0]["fileInfo"]["url"]
    return url_output


def upload_img_from_disk_server_and_get_link(file_name):
    data = {'files': open(file_name, 'rb')}
    url = requests.post(url_api_save_file, files=data)
    url_output = url_server_save_file + url.json()["results"][0]["fileInfo"]["url"]
    return url_output


def read_url_img_to_array(url):
    if url[-4:] == "HEIC":
        response = requests.get(url)
        bytesIo = response.content
        i = pyheif.read(bytesIo)
        pi = Image.frombytes(
            mode=i.mode, size=i.size, data=i.data)
        img = np.array(pi)
        """Không cần resize vì qua model đã resize(1000, 1000)"""

    # response = requests.get(url)
    # img = Image.open(BytesIO(response.content))
    # img = np.array(img)
    # https://pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
    elif url[:-4] == "http":
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = np.array(img)
    else:
        try:
            img = cv2.imread(url)
        except Exception as e:
            print("Lỗi đọc ảnh từ url: ", e)
            img = None
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
    return img


if __name__ == '__main__':
    path_image = '/home/gg_greenlab/Pictures/Sang.png'
    img_arr = cv2.imread(path_image)
    url_output = upload_img_from_disk("test", img_arr)
    print(url_output)
    # img_arr = read_url_img_to_array(url_output)
    # img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    # a = 0
    # cv2.imwrite("/home/gg-greenlab/Downloads/index1.jpeg", img_arr)