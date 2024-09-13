import os
import sys
import requests
from PIL import Image
import numpy as np
import cv2
import pyheif
from skimage import io


def read_url_img_to_array(url):
    if url[-4:] == "HEIC":
        response = requests.get(url)
        bytesIo = response.content
        i = pyheif.read(bytesIo)
        pi = Image.frombytes(
            mode=i.mode, size=i.size, data=i.data)
        img = np.array(pi)
        # img2 = img
        img2 = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

    # response = requests.get(url)
    # img = Image.open(BytesIO(response.content))
    # img = np.array(img)
    # https://pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
    else:
        img2 = io.imread(url)
    return img2


def test_get_size():
    file = "/home/gg_greenlab/Desktop/3a05b66c-50a3-cee5-6b33-99d5f8a3ab3e.HEIC"
    # file = "/home/gg_greenlab/Desktop/3a05b832-14b7-0192-b9c1-b1e657702419.jpeg"
    url = 'https://file.erp.clover.edu.vn/file-storage/2022/08/20220816/3a05b66c-50a3-cee5-6b33-99d5f8a3ab3e.HEIC'
    # url = 'https://file.erp.clover.edu.vn/file-storage/2022/08/20220816/3a05b832-14b7-0192-b9c1-b1e657702419.JPG'
    size = os.path.getsize(file)
    print(size)
    img_array = read_url_img_to_array(url)
    array_size = sys.getsizeof(img_array)
    print(array_size)

    array_size_nbyte = img_array.nbytes
    print(array_size_nbyte)
    print(array_size_nbyte/1024/1024)

"""
Phân tích:
+ Có cần reset lại GPU sau mỗi lần lọc, reset như thế nào?
+ Xử lí đồng thời tối đa được bao nhiêu hình, dung lượng tổng các hình là bao nhiêu MB, mất thời gian bao lâu?
+ Chia ra từng giai đoạn với tối đa số hình thì mất thời gian bao lâu?
+ Tại sao sau mỗi lần lọc dung lượng GPU chỉ tăng thêm khi số lượng hình gửi lần sau lớn hơn lần trước và 
giữ nguyên ở dung lượng đó?

REPORT:
+ Xử lí song song(batch-size):
    + Tối đa chạy cùng lúc 112 hình, tổng dung lượng:  161MBytes, thời gian xử lí: (150s)10s(8049-1209=7020)
    + RAM GPU Không quan trọng dung lượng mỗi ảnh vì tất cả ảnh qua model det face resize(1000, 1000), quan trọng số lượng ảnh.
    + 1 ảnh HIEC 1MBytes xử lí (1.7s)0.4s. cost 80MB GPU
    + 1 ảnh jpeg 3MB xử lí (2s)0.42s. cost 80MB GPU
    
    + Kết luận: thời gian xử lí hoàn toàn phụ thuộc vào tốc độ đọc ảnh từ server file, ảnh càng to thời gian xử lí càng lâu.
    + Do đó xử dụng batch size không có ý nghĩa nhiều ở ngữ cảnh này.
+ Xử lí tuần tự: 
    + Cùng lúc 20 hình: 41432873(40MB) (total 28s)2.11s GPU(3323-1209MB=2294M)
    + 112 hinh batch-size=10 146s GPU(1985-1209=956MB)
    + 112 hinh batch-size=1 150s GPU(1279-1209=80MB)
    + 112 hinh batch-size=32 143s GPU(1279-1209=80MB)
    + 112 hinh batch-size=64 150s GPU(1279-1209=80MB)
    + 112 hinh batch-size=5 144s GPU(1279-1209=80MB)
"""


def get_image_from_server_file():
    url_api_save_file = 'https://file.erp.clover.edu.vn/api/files'
    params = {'fileIds': ["3a05b664-b6e8-ff54-c8cc-b408c15eef78"]}
    result = requests.get(url_api_save_file, params=params)
    import pprint
    pprint.pprint(result.content)


if __name__ == '__main__':
    # response = requests.get(url)
    # bytesIo = response.content
    # bytes_of_url_image = len(bytesIo)
    get_image_from_server_file()

