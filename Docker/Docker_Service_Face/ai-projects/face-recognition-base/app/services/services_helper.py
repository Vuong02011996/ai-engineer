import datetime
import time
import numpy as np
import os
import requests
import json
import cv2
from glob import glob

from bson import ObjectId

from app.app_utils.file_io_untils import upload_video_from_disk_server_and_get_link, \
    upload_img_from_disk_server_and_get_link, upload_img_from_disk

from app.mongo_dal.camera_dal import CameraDAL
from core.main.main_utils.draw import draw_region

camera_dal = CameraDAL()

url_get_user_notify = os.getenv("url_get_user_notify")
url_notify = os.getenv("url_notify")
username_get_token = os.getenv("username_get_token")
password_get_token = os.getenv("password_get_token")


def nparray_to_bytebuffer(image):
    """
    Convert the numpy array to bytes buffer
    It's used to send the np.array via request
    The server side can interpret the Io.Bytes Buffer
    Args:
        image (np.array): HxWx3

    Returns:
        byte_img (bytes): bytes image
    """
    if isinstance(image, np.ndarray):
        flag, frame = cv2.imencode(".jpg", image)
        if flag:
            frame = frame.tobytes()
            return frame
        else:
            raise RuntimeError("The image's format is not correct")
    else:
        raise RuntimeError("The data is not nd.array")


def get_frame_url_from_cam(url_cam):
    cap = cv2.VideoCapture(url_cam)
    ret, frame = cap.read()
    if ret:
        frame_url = upload_img_from_disk(
            img_arr=frame)
    else:
        frame_url = None
    return frame_url


def get_utc_time_from_datetime(date_time):
    seconds = date_time.timestamp()
    utc_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(seconds))
    return utc_time


def get_num_page_from_limit(list_object_id, limit):
    if len(list_object_id) % limit > 0:
        num_page = int(len(list_object_id) / limit + 1)
    else:
        num_page = int(len(list_object_id) / limit)
    return num_page


def pagination(limit, new_item, page):
    # Pagination - phan trang
    if limit is None:
        data_out = {
            "status": 200,
            "title": "Get all data roll call successfully.",
            "data": new_item,
            "meta": {
                "pagination": {
                    "total": len(new_item),
                    "current_page": 1,
                    "total_pages": 1
                }
            },
        }
    else:
        num_page = get_num_page_from_limit(new_item, limit)
        if page <= num_page:
            start_item = (page - 1) * limit
            list_object_info_page = []
            for i in range(start_item, np.minimum(start_item + limit, len(new_item))):
                list_object_info_page.append(new_item[i])

        data_out = {
            "status": 200,
            "title": "Get data successfully.",
            "data": new_item,
            "meta": {
                "pagination": {
                    "total": len(new_item),
                    "current_page": page,
                    "total_pages": num_page
                }
            },
        }
    return data_out


def get_info_camera(url_cam):
    cap = cv2.VideoCapture(url_cam)
    # command and params for ffmpeg
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, width, height


def list_images_to_video_cv2(video_name, list_image):
    frame = cv2.imread(list_image[0])
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name,
                            cv2.VideoWriter_fourcc(*'vp80'),  # X264, MJPG, MPEG, 'vp80', MP4V
                            25, (width, height))
    for image in list_image:
        img = cv2.imread(image)
        video.write(img)
    video.release()


def get_list_image_url_and_clip_url(item, object_dal, folder_frame):

    list_image = glob(folder_frame + "/*.png")
    list_image.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    # clip url
    if item.get("clip_url") is None:
        start_time = time.time()
        video_name = folder_frame + '/video_cv2.webm'
        if os.path.exists(video_name) is False:
            list_images_to_video_cv2(video_name, list_image)
        print("list_images_to_video_cv2 cost : ", time.time() - start_time)
        clip_url = upload_video_from_disk_server_and_get_link(video_name)
        #  Update object info to mongDB
        objects_data_elem = {
            "clip_url": clip_url,
            # "created_at": datetime.datetime.now(),
        }
        object_dal.update_document([item["_id"]], [objects_data_elem])
    else:
        clip_url = item["clip_url"]

    # image url
    if item.get("image_url") is None:
        image_url = upload_img_from_disk_server_and_get_link(list_image[0])
        objects_data_elem = {
            "image_url": image_url,
            # "created_at": datetime.datetime.now(),
        }
        object_dal.update_document([item["_id"]], [objects_data_elem])
    else:
        image_url = item["image_url"]

    list_image_url = [image_url]
    return clip_url, list_image_url


def check_save_video():
    folder_frame = "/media/vuong/AI1/Data_clover/Image/test_video/Sleepless_Region_0"
    video_name = folder_frame + '/video_cv2.webm'
    list_image = glob(folder_frame + "/*.png")
    list_image.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    start_time = time.time()
    list_images_to_video_cv2(video_name, list_image)
    print("image to video cost : ", time.time() - start_time)
    clip_url = upload_video_from_disk_server_and_get_link(video_name)
    print(clip_url)


def update_status_job(id_cam, item_cam, process_name, status_process, job="roll_call"):
    mongo_id = ObjectId(id_cam)
    if item_cam.get("jobs_cam") is not None:
        jobs_cam_update = item_cam["jobs_cam"]
    else:
        jobs_cam_update = {}

    jobs_cam_update[job]["process_name"] = process_name
    jobs_cam_update[job]["status_process"] = status_process
    data_update = {
        "jobs_cam": jobs_cam_update,
    }
    camera_dal.update({"_id": mongo_id}, data_update)


def test_region_from_fe(cap, region_track):
    # self.region track yêu cầu: Hồng(tl-0) -> trắng(tr-1) ->  xanh lam(br-3) -> đỏ(bl-2),
    ret, frame_ori = cap.read()
    # frame_ori = cv2.rectangle(frame_ori, tuple(coordinates[0]), tuple(coordinates[2]), (0, 0, 255), 2)
    regions = np.array(region_track)
    # Nếu trường hợp tọa độ là mảng 3 chiều(nhiều vùng)
    # Ta phải xử lí từng vùng sau đó concat các head từ detections lại với nhau.
    if regions.ndim == 3:
        for region in regions:
            frame_ori = cv2.circle(frame_ori, tuple(region[0]), radius=5, color=(255, 0, 255),
                                   thickness=10)  # Hồng
            frame_ori = cv2.circle(frame_ori, tuple(region[1]), radius=5, color=(255, 255, 255),
                                   thickness=10)  # trắng
            frame_ori = cv2.circle(frame_ori, tuple(region[3]), radius=5, color=(0, 0, 255),
                                   thickness=10)  # xanh lam
            frame_ori = cv2.circle(frame_ori, tuple(region[2]), radius=5, color=(255, 0, 0), thickness=10)  # đỏ
    else:
        frame_ori = cv2.circle(frame_ori, tuple(region_track[0]), radius=5, color=(255, 0, 255), thickness=10) # Hồng
        frame_ori = cv2.circle(frame_ori, tuple(region_track[1]), radius=5, color=(255, 255, 255), thickness=10) # trắng
        frame_ori = cv2.circle(frame_ori, tuple(region_track[3]), radius=5, color=(0, 0, 255), thickness=10) # xanh lam
        frame_ori = cv2.circle(frame_ori, tuple(region_track[2]), radius=5, color=(255, 0, 0), thickness=10) # đỏ

    frame_ori = draw_region(frame_ori, region_track)
    cv2.imshow('output_roll_call', cv2.resize(frame_ori, (800, 500)))
    cv2.waitKey(0)


def get_coordinates_from_item_cam(item_cam, width, height, show_region):
    list_coordinates = []
    # resize coordinates
    if item_cam.get("jobs_cam") is None \
            or item_cam["jobs_cam"].get(show_region) is None \
            or item_cam["jobs_cam"][show_region].get("coordinates") is None \
            or len(item_cam["jobs_cam"][show_region]["coordinates"]) == 0:
        list_coordinates = None
    else:
        coordinates = item_cam["jobs_cam"][show_region]["coordinates"]
        print("coordinates: ", coordinates)
        # coordinates:  [{'name_regions': 'Vùng 1', 'coord': [[0.68, 0.12], [0.71, 0.5], [0.91, 0.1], [0.95, 0.48]]},
        #                {'name_regions': 'Vùng 1', 'coord': [[0.68, 0.12], [0.71, 0.5], [0.91, 0.1], [0.95, 0.48]]},..]
        for item_coord in coordinates:
            coord = item_coord["coord"]
            for i in range(len(coord)):
                coord[i][0] *= width
                coord[i][1] *= height
                coord[i] = list(map(int, coord[i]))
            list_coordinates.append(coord)

    return list_coordinates


def get_users_and_sent_notify(class_id, message, image_url, access_token):
    # class_id = "3a02d140-4827-544e-3eb9-906cd9bcd61e"
    # url = "https://clover-api.greenglobal.com.vn/api/employee-accounts/classId/" + class_id
    # access_token = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkZERTI2MThCRTAxMzBEMTk0QzlGQkYxNzNEQTQxM0QzIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2ODI0OTAxNDMsImV4cCI6MTcxNDAyNjE0MywiaXNzIjoiaHR0cHM6Ly9zc28uZ3JlZW5nbG9iYWwuY29tLnZuIiwiYXVkIjoiRXJwIiwiY2xpZW50X2lkIjoiRXJwX0FwcCIsInN1YiI6IjM5ZmM3ODViLTM5NmYtMThkMi0yNGVlLTU0N2YzMDc5OWE4MSIsImF1dGhfdGltZSI6MTY4MjQ5MDE0MywiaWRwIjoibG9jYWwiLCJyb2xlIjoiYWRtaW4iLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOiJGYWxzZSIsImVtYWlsIjoiYWRtaW5AYWJwLmlvIiwiZW1haWxfdmVyaWZpZWQiOiJGYWxzZSIsIm5hbWUiOiJhZG1pbiIsImlhdCI6MTY4MjQ5MDE0Mywic2NvcGUiOlsiRXJwIl0sImFtciI6WyJwd2QiXX0.lDR4I8cW5ZvbQS7cn7ZktXW8PdhBbJSNPZdjkUcDDrl4OiVaQDYzhUxd8AhXq0SpXPQJPKs2RxlFCr0-O5BiCS7GgsxWfyFupOBPXJDKpUvktv_XIr-Cr9AEbtK141lIJI6maBueAKPVr--EdACMnlEcVMpwpfm0IeNaJRDz6cXZ4VTt0DA0MH9NEvo_Xj1XSPruBZG7adZ1e5zn9YkHzvFDRgRbXBU9JUCF7BT_-Q8sYutoOcnaAv6cMKYM1uRBS-KTPVitUqkwa3aMD_I0hNV9BgHExEj3F6EYAND8NpQtYlvIMotL8h7LNmKOLhyILV8BquG33oub2QqMnfdhEw'
    print("class_id: ", class_id)
    url_get_user_notify_full = url_get_user_notify + class_id
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.request("GET", url_get_user_notify_full, headers=headers, data=payload)
    data = response.json()

    # and data.get('Unauthorized') is not None
    if len(data) > 0 and data[0].get("appUserId") is not None:
        headers_noti = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        # users = "39fef9cf-d78b-4a6e-bee1-a8112875da1b"
        # url = "https://clover-api.greenglobal.com.vn/api/notification/publish"
        print("data: ", data)
        for item_user in data:
            print("item_user: ", item_user)
            users = item_user["appUserId"]
            payload = json.dumps({
                "users": [
                    users
                ],
                "title": message,
                "imageURL": image_url,
                "message": message,
                # "moduleType": "HEALTH"
            })
            response = requests.request("POST", url_notify, headers=headers_noti, data=payload)
            # print("response.json() after sent noty: ", response.json())
    else:
        print("No users to sent noty len(data) = 0 or 'Unauthorized'")
        """
        Lỗi Unauthorized chú ý kiểm tra file env đang chạy là gì rồi , đặc biệt chạy bằng pm2 
        Rồi mới get token đúng tài khoản admin trên server đó.
        """


def get_token_login():
    url = "https://sso.greenglobal.com.vn/connect/token"

    payload = 'username=' + username_get_token + '&password=' + password_get_token + '&grant_type=password'
    # payload = 'username=hao&password=123456&grant_type=password'
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'authorization': 'Basic RXJwX0FwcDoxcTJ3M0Uq',
        'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    access_token = response.json()["access_token"]
    return access_token


def check_sent_noty():
    class_id = "3a02d140-4827-544e-3eb9-906cd9bcd61e"
    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkZERTI2MThCRTAxMzBEMTk0QzlGQkYxNzNEQTQxM0QzIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2ODI1NjMyMjYsImV4cCI6MTcxNDA5OTIyNiwiaXNzIjoiaHR0cHM6Ly9zc28uZ3JlZW5nbG9iYWwuY29tLnZuIiwiYXVkIjoiRXJwIiwiY2xpZW50X2lkIjoiRXJwX0FwcCIsInN1YiI6IjM5ZmM3ODViLTM5NmYtMThkMi0yNGVlLTU0N2YzMDc5OWE4MSIsImF1dGhfdGltZSI6MTY4MjU2MzIyNiwiaWRwIjoibG9jYWwiLCJyb2xlIjoiYWRtaW4iLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOiJGYWxzZSIsImVtYWlsIjoiYWRtaW5AYWJwLmlvIiwiZW1haWxfdmVyaWZpZWQiOiJGYWxzZSIsIm5hbWUiOiJhZG1pbiIsImlhdCI6MTY4MjU2MzIyNiwic2NvcGUiOlsiYWRkcmVzcyIsImVtYWlsIiwiRXJwIiwib3BlbmlkIiwicGhvbmUiLCJwcm9maWxlIiwicm9sZSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.E7NGEknLnrvvFTi7zEmagDbJrDRkGDfUIOJLlanR0F-lAnduI3yn1K0cawE4pKaNNFebGHSXo9VbjiRuOYbkjw_sAalYDKr1z7wjzd4gW1DoF6IFqOMXdw6BanTVdzqdXfaFI_QqtOh_r2djVIz41mNilcumunHrX6AaTiqewLOippTMY5JZmb10aSEOdAUa0QzMbqfsfM09AwU2zZzwcTOpZGHMiJcIHukiP-Z1rnHpxhLpR93ZIA-h5YTBC0Jm2vEQ1i2MR9Alihi6gvbzdcrSfEG2u1sf0Ie1swa3PEiQaEVbVduIQZtg-Iu3IQTVUz9SnpJWwmDFJPSY1kkGtw"
    print("class_id: ", class_id)
    url_get_user_notify_full = url_get_user_notify + class_id

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.request("GET", url_get_user_notify_full, headers=headers, data=payload)
    data = response.json()

    if len(data) > 0:
        headers_noti = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        # users = "39fef9cf-d78b-4a6e-bee1-a8112875da1b"
        # url = "https://clover-api.greenglobal.com.vn/api/notification/publish"
        for item_user in data:
            users = item_user["appUserId"]

    else:
        print("No users to sent noty len(data) = 0")


if __name__ == '__main__':
    # check_sent_noty()
    # print(str(datetime.datetime.now()))
    timestamp = str(datetime.datetime.now())
    datetime_obj = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    formatted_time = datetime_obj.strftime("%H:%M:%S %Y-%m-%d")
    print("formatted_time: ", formatted_time)