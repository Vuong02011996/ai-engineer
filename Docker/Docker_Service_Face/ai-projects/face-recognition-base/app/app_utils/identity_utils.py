import time
import requests
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import os
from glob import glob
import random
from datetime import datetime

# from app.app_utils.minio_utils import upload_image, read_stream_img
from app.app_utils.file_io_untils import upload_img_from_disk, read_url_img_to_array

from core.main.main_utils.helper import read_url_img_to_array
from app.app_utils.face_local_utils_v2 import FaceLocalUtils
from app.app_utils.face_local_utils import FaceLocalUtils as FaceLocalUtils_old
from app.milvus_dal.clover_dal import MilvusCloverDAL
from app.mongo_dal.identity_dal import IdentityDAL

face_util = FaceLocalUtils()
milvus_dal = MilvusCloverDAL()
identity_dal = IdentityDAL()


def get_a_facial_vector_and_an_url(url, facial_vector, image_face, image_rgb, frame_index, list_image_url,
                                   list_facial_vector):
    name_url = url.split("/")[-1].split(".")[0]
    image_url = upload_img_from_disk(image_name="origin_" + name_url + "_" + str(frame_index), img_arr=image_face)
    list_image_url.append(image_url)
    list_facial_vector.append(facial_vector)


def get_a_facial_vector(facial_vector, list_facial_vector):
    list_facial_vector.append(facial_vector)


def get_matching_face_ids_and_original_url(data, update_ai=False, det_threshold = 0.6):
    """
    data list of url images or video
    Example: ["https://minio.core.greenlabs.ai/local/avatar/8nn644vh3tw8wi6p97c7hmzt2kjyeo.jpg",
              "https://minio.core.greenlabs.ai/local/avatar/8nn644vh3tw8wi6p97c7hmzt2kjyeo.mp4", ..]
    :param data:
    :return: matching_face_ids:  [{"url": "https_url",
                                "face_id": id milvus}, ...]
            original_url: url of image rgb size original
    """

    # list_image_url = []
    list_image_url_ori = []
    list_facial_vector = []
    list_accuracy_face_detect = []
    list_w_h = []

    for idx, url in enumerate(data):
        if url[-4:].lower() in [".mp4", ".mov", ".avi"]:
            cap = cv2.VideoCapture(url)
            frame_index = 0
            frame_using = 0
            while cap.isOpened():
                ret, image_raw = cap.read()
                if not ret:
                    break

                if frame_using != 0 and frame_index % frame_using != 0:
                    frame_index += 1
                    continue
                frame_using += 4
                h, w, _ = image_raw.shape
                # Filter image size < (300, 300)
                if w < 100 or h < 100:
                    print("Image have w, h < 100")
                    return None
                # Some video must transpose
                if w > h:
                    image_raw = cv2.transpose(image_raw)

                image_rgb = image_raw
                face_util_old = FaceLocalUtils_old()
                facial_vector, image_face, accuracy_face_detect = face_util_old.detect_face_and_get_embedding_an_image(image_rgb)
                # facial_vector, image_face, accuracy_face_detect = face_util.detect_face_and_get_embedding_an_image_scrfd(image_rgb, det_threshold=det_threshold, video=True)

                if facial_vector is None:
                    continue

                get_a_facial_vector_and_an_url(url, facial_vector, image_face, image_rgb, frame_index, list_image_url,
                                               list_facial_vector)
                list_image_url_ori.append(url)
                list_w_h.append([w, h])
                list_accuracy_face_detect.append(accuracy_face_detect)

                frame_index += 1
                print("frame_index: ", frame_index)
            cap.release()
        else:
            arr_img = read_url_img_to_array(url)
            #  Lỗi url ảnh
            if arr_img is None:
                continue
            h, w, _ = arr_img.shape
            # Filter image size < (300, 300)
            if w < 100 or h < 100:
                print("w < 100 or h < 100")
                return None
            image_rgb = cv2.cvtColor(arr_img, cv2.COLOR_BGR2RGB)
            face_util_old = FaceLocalUtils_old()
            facial_vector, image_face, accuracy_face_detect = face_util_old.detect_face_and_get_embedding_an_image(image_rgb)
            # facial_vector, image_face, accuracy_face_detect = face_util.detect_face_and_get_embedding_an_image_scrfd(image_rgb, det_threshold=det_threshold)

            if facial_vector is None:
                continue

            # chỉ chạy để lay url khuon mat, xem lại khuôn mặt đã đăng kí chuẩn không, TH nhận diện không ra
            # do dung server file ben clover
            # get_a_facial_vector_and_an_url(url, facial_vector, image_face, image_rgb, idx, list_image_url,
            #                                list_facial_vector)
            list_image_url_ori.append(url)
            list_facial_vector.append(facial_vector)
            list_w_h.append([w, h])
            list_accuracy_face_detect.append(accuracy_face_detect)

    if len(list_facial_vector) == 0:
        return None

    # assert len(list_facial_vector) == len(list_image_url) == len(list_image_url_ori)
    list_face_id = milvus_dal.insert_data(list_facial_vector)
    matching_face_ids = []
    for i, face_id in enumerate(list_face_id):
        matching_face_ids.append({
            # 'url_face': list_image_url[i],
            "face_id": face_id,
            "accuracy_face_detect": list_accuracy_face_detect[i],
            "url_ori": list_image_url_ori[i],
            "width_img": list_w_h[i][0],
            "height_img": list_w_h[i][1],
        })

    return matching_face_ids


def get_matching_face_ids_ver_oryza(data):
    """
    data list of url images or video
    Example: ["https://minio.core.greenlabs.ai/local/avatar/8nn644vh3tw8wi6p97c7hmzt2kjyeo.jpg",
              "https://minio.core.greenlabs.ai/local/avatar/8nn644vh3tw8wi6p97c7hmzt2kjyeo.mp4", ..]
    :param data:
    :return: matching_face_ids:  [{"url": "https_url",
                                "face_id": id milvus}, ...]
            original_url: url of image rgb size original
    """

    # list_image_url = []
    list_image_url_ori = []
    list_facial_vector = []
    list_accuracy_face_detect = []
    list_w_h = []

    for idx, url in enumerate(data):
        arr_img = read_url_img_to_array(url)
        #  Lỗi url ảnh
        if arr_img is None:
            continue
        h, w, _ = arr_img.shape
        print("width: ", w)
        print("height: ", h)

        # Filter image size < (300, 300)
        if w < 50 or h < 50:
            print("w < 100 or h < 100")
            continue
            # return None
        image_rgb = cv2.cvtColor(arr_img, cv2.COLOR_BGR2RGB)
        face_util_old = FaceLocalUtils_old()
        facial_vector, image_face, accuracy_face_detect = face_util_old.detect_face_and_get_embedding_an_image(image_rgb)

        if facial_vector is None:
            print("Image no facial_vector")
            continue

        # chỉ chạy để lay url khuon mat, xem lại khuôn mặt đã đăng kí chuẩn không, TH nhận diện không ra
        # do dung server file ben clover
        # get_a_facial_vector_and_an_url(url, facial_vector, image_face, image_rgb, idx, list_image_url,
        #                                list_facial_vector)
        get_a_facial_vector(facial_vector, list_facial_vector)
        list_image_url_ori.append(url)
        list_w_h.append([w, h])
        list_accuracy_face_detect.append(accuracy_face_detect)

    if len(list_facial_vector) == 0:
        return None

    # assert len(list_facial_vector) == len(list_image_url) == len(list_image_url_ori)
    list_face_id = milvus_dal.insert_data(list_facial_vector)
    matching_face_ids = []
    for i, face_id in enumerate(list_face_id):
        matching_face_ids.append({
            # 'url_face': list_image_url[i],
            "face_id": face_id,
            "accuracy_face_detect": list_accuracy_face_detect[i],
            "url_ori": list_image_url_ori[i],
            "width_img": list_w_h[i][0],
            "height_img": list_w_h[i][1],
        })

    return matching_face_ids


def get_data_matching_face_ids_v3(url):
    arr_img = read_url_img_to_array(url)
    image_rgb = cv2.cvtColor(arr_img, cv2.COLOR_BGR2RGB)
    facial_vector = face_util.get_facial_vector_from_image_face(image_rgb)
    list_face_id = milvus_dal.insert_data([facial_vector])
    matching_face_ids = [{
        'url_face': url,
        "face_id": list_face_id[0],
        "types": "AI",
        "threshold": 0.35,
    }]
    return matching_face_ids


def concatenate_face_one_identity(name):
    pipeline = [
        {"$match": {"type": 'Hoc Sinh', "name": name}}]
    data = list(identity_dal.aggregate(pipeline))
    list_url = list(map(lambda x: x['url_face'], data[0]["matching_face_ids"]))
    num_col = 10
    combine_row_img = None
    combine_all_img = None
    for i, url_face in enumerate(list_url):
        # img_array = read_stream_img(url_face)
        img_array = read_url_img_to_array(url_face)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        img_array = cv2.resize(img_array, (112, 112), interpolation=cv2.INTER_AREA)

        if combine_row_img is None:
            combine_row_img = img_array
        else:
            combine_row_img = np.hstack((combine_row_img, img_array))

        if (i + 1) % num_col == 0:
            # cv2.imwrite("image_test/" + name + ".png", combine_row_img)
            if combine_all_img is None:
                combine_all_img = combine_row_img
            else:
                combine_all_img = np.vstack((combine_all_img, combine_row_img))
            combine_row_img = None
    # if last row not enough num_col image
    if combine_row_img is not None:
        for i in range(int(num_col - (combine_row_img.shape[1]/112))):
            combine_row_img = np.hstack((combine_row_img, np.zeros((112, 112, 3), dtype=np.uint8)))
        if combine_all_img is not None:
            combine_all_img = np.vstack((combine_all_img, combine_row_img))
        else:
            combine_all_img = combine_row_img

    # url = upload_image(combine_all_img, folder_name="identity", image_name=name)
    url = upload_img_from_disk(image_name=name, img_arr=combine_all_img)
    cv2.imwrite("image_test/" + name + ".png", combine_all_img)
    return url


def insert_folder_video_to_sign_in_identity(folder_path="/home/vuong/Videos/PreSchool"):
    list_file_video = glob(f"{folder_path}/*.mp4")
    user_id = random.randint(1, 1e6)
    transpose = True
    if len(list_file_video) == 0:
        data_out = {"status": True, "status_code": 200, "message": "Folder not found video"}
        return data_out
    for idx, video in enumerate(list_file_video):
        print(f"Processing Video: {idx+1}/{len(list_file_video)}")
        if video[-4:].lower() in [".mp4", ".mov", ".avi"]:
            original_url_list = []
            list_image_url = []
            list_facial_vector = []
            cap = cv2.VideoCapture(video)
            frame_index = 0
            frame_using = 0
            while cap.isOpened():
                ret, image_raw = cap.read()
                if frame_using != 0 and frame_index % frame_using != 0:
                    frame_index += 1
                    continue
                frame_using += 3
                frame_index += 1
                print("frame_index: ", frame_index)
                if frame_index == 115:
                    a = 0

                if not ret:
                    break
                # if transpose:
                #     image_raw = cv2.transpose(image_raw)
                image_rgb = cv2.cvtColor(image_raw, cv2.COLOR_BGR2RGB)
                facial_vector, image_face, accuracy_face_detect = face_util.detect_face_and_get_embedding_an_image_scrfd(image_rgb)
                if facial_vector is None:
                    print("Not found any face in frame")
                    continue
                get_a_facial_vector_and_an_url(video, facial_vector, image_face, image_rgb, frame_index, list_image_url,
                                               list_facial_vector, original_url_list)
            cap.release()
            if len(list_facial_vector) == 0:
                print("video {} no detect any face".format(video))
                return 0
            list_face_id = milvus_dal.insert_data(list_facial_vector)
            matching_face_ids = []
            for i, face_id in enumerate(list_face_id):
                matching_face_ids.append({
                    'url_face': list_image_url[i],
                    "face_id": face_id
                })

            if "Cô" in video.split("/")[-1][:-4]:
                types = "Giao Vien"
            else:
                types = "Hoc Sinh"
            item = identity_dal.create_one(
                {
                    "name": video.split("/")[-1][:-4],
                    "user_id": str(user_id + idx),
                    "type": types,
                    "status": "testing",
                    "matching_face_ids": matching_face_ids,
                    "created_at": datetime.now(),
                    "original_url": original_url_list[0],
                }
            )

    data_out = {"status": True, "status_code": 200, "message": "Register folder successfully"}
    return data_out


if __name__ == '__main__':
    insert_folder_video_to_sign_in_identity(folder_path="/home/vuong/Desktop/Data/Clover/Video Register")