import requests
import cv2

# + swagger : https://erp-clover-file.demo.greenglobal.com.vn/swagger/index.html

# url_api = 'https://erp-clover-file.demo.greenglobal.com.vn/api/files'
url_api_save_file='https://file.erp.clover.edu.vn/api/files'
# url_server = 'https://erp-clover-file.demo.greenglobal.com.vn'
url_server_save_file='https://file.erp.clover.edu.vn'
# data = {'files': open('/storages/data/DATA/Clover_data/Frame_Process/6203743cc5d991baa520b624_safe_region/track_1/video.mp4', 'rb')}
data = {'files': open('DATA/data/DATA/Clover_data/Image_URL/admin_HikC@mera_58.186.75.67_5555.png', 'rb')}

# array_img = cv2.imread('/home/gg-greenlab/Downloads/index.jpg')
# data = {"files:": array_img}
url = requests.post(url_api_save_file, files=data)
url_output = url_server_save_file + url.json()["results"][0]["fileInfo"]["url"]
print(url_output)
print(url.json()["results"][0]["fileInfo"]["url"])
print(url.json())