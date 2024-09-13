import traceback
from datetime import datetime

import cv2
import numpy as np
import requests
import time
from collections import Counter
import os

from sentry_sdk import capture_message

from app.app_utils.roll_pitch_yaw_utils import get_Roll_Pitch_Yaw_new, is_frontal_face
from app.mongo_dal.identity_dal import IdentityDAL
# from core.main.main_utils.box_utils import extend_bbox
# from core.main.main_utils.draw import draw_det_when_track, draw_box_and_landmark
from core.main.main_utils.helper import convert_np_array_to_base64, read_url_img_to_array, align_face, get_url_as_base64
from app.milvus_dal.clover_dal import MilvusCloverDAL


milvus_staging_dal = MilvusCloverDAL()
identity_dal = IdentityDAL()

# global variables
MIN_ROLL, MIN_PITCH, MIN_YAW = 90, 90, 90


class FaceLocalUtils(object):
    def __init__(self, det_threshold_srcfd=0.7, image_size_embedding=(112, 112),
                 distance_threshold=0.5):
        self.det_threshold_srcfd = det_threshold_srcfd
        self.image_size_embedding = image_size_embedding
        self.distance_threshold = distance_threshold
        port_model_insight = int(os.getenv("port_model_insight"))
        ip_run_service_insight = os.getenv("ip_run_service_insight")
        self.api_insightface = "http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract"

    def get_base64_box_face(self, box_face, arr_img, align=True, landmark=None):
        box_face = list(map(int, box_face[:4]))
        image_face = arr_img[box_face[1]:box_face[3], box_face[0]:box_face[2]]
        # cv2.imshow("Samed", image_face)
        # cv2.waitKey(0)
        if 0 in image_face.shape:
            # Take face error
            return None, None
        if align and landmark is not None:
            image_face_resize = align_face(arr_img, box_face, landmark)
        else:
            image_face_resize = cv2.resize(image_face, self.image_size_embedding, interpolation=cv2.INTER_AREA)
        # image_face_resize = cv2.cvtColor(image_face_resize, cv2.COLOR_BGR2RGB)
        face_base64 = convert_np_array_to_base64(image_face_resize)
        return face_base64, image_face

    def get_facial_vector_from_image_face(self, image_face):
        image_face_resize = cv2.resize(image_face, self.image_size_embedding, interpolation=cv2.INTER_AREA)
        face_base64 = convert_np_array_to_base64(image_face_resize)
        req = {"images": {"data": [face_base64]}, "embed_only": True}
        port_model_insight = int(os.getenv("port_model_insight"))
        ip_run_service_insight = os.getenv("ip_run_service_insight")
        resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
        data = resp.json()
        facial_vector = data["data"][0]["vec"]
        return facial_vector

    def detect_batch_img_array_scrfd(self, list_img_array, data_in, det_threshold):
        """
        :param list_img_array: list image array [[height, width, 3], [height, width, 3], ...]
        :param det_threshold
        :return:
        box_detect: [B, N, 4]
        landmark_detect: [B, N, 5, 2]
        accuracy_detect: [B, N, 1]
        B: number of batch or len(list_img_array)
        N: number of box face in each image.

        """
        target = []
        for img_arr in data_in:
            # target.append(convert_np_array_to_base64(img_arr))
            target.append(get_url_as_base64(img_arr["image"]))

        req = {"images": {"data": target}, "threshold": det_threshold, "return_landmarks": True, "embed_only": False,
               "extract_embedding": False}
        resp = requests.post(self.api_insightface, json=req)
        data = resp.json()
        a = 0
        box_detect = []
        landmark_detect = []
        accuracy_detect = []
        for faces_img in data["data"]:
            box_detect.append(list(map(lambda d: d['bbox'], faces_img['faces'])))
            landmark_detect.append(list(map(lambda d: d['landmarks'], faces_img['faces'])))
            accuracy_detect.append(list(map(lambda d: d['prob'], faces_img['faces'])))
        return box_detect, landmark_detect, accuracy_detect

    def detect_and_get_embedding_all_face_of_list_img_array_scrfd(self, list_img_array, data_in, resize=True):
        """
        Take all face in image(for group)
        Get embedding, bbox face from list_img_array
        :param list_img_array: list numpy array [N, height, width, 3]
        :param resize
        :return: list embedding, list bbox face, list id image , all the same length, length is number of face in all image.
        """
        box_detect, landmark_detect, accuracy_detect = self.detect_batch_img_array_scrfd(list_img_array, data_in, det_threshold=0.6)
        assert len(list_img_array) == len(box_detect) == len(accuracy_detect)

        # # Show test model detect image
        # for idx_img in range(len(list_img_array)):
        #     boxes = box_detect[idx_img]
        #     image_show = draw_box_and_landmark(list_img_array[idx_img], boxes, landmark=None)
        #     cv2.imshow("test", image_show)
        #     cv2.waitKey(0)

        list_facial_vector_all_image = []
        list_image_face_all_image = []
        list_id_image = []

        for id_image in range(len(box_detect)):
            arr_img = list_img_array[id_image]
            boxes_face = box_detect[id_image]
            list_face_base64 = []
            for idx, box_face in enumerate(boxes_face):
                face_base64, image_face = self.get_base64_box_face(box_face, arr_img, align=True)
                list_face_base64.append(face_base64)
                list_image_face_all_image.append(image_face)
                list_id_image.append(id_image)

            req = {"images": {"data": list_face_base64}, "embed_only": True}
            resp = requests.post(self.api_insightface, json=req)
            data = resp.json()
            for idx_face in range(len(data["data"])):
                list_facial_vector_all_image.append(data["data"][idx_face]["vec"])

        assert len(list_facial_vector_all_image) == len(list_image_face_all_image) == len(list_id_image)
        return list_image_face_all_image, list_facial_vector_all_image, list_id_image

    def get_identity_list_facial_vector(self, list_facial_vector):
        """
        Get list embedding vector of a group(can one vector), search in milvus , mongo
        and return a name closest matching with all vector; closest name is name have maximum number of vector match.
        Example: list_facial_vector = [[N], ...], N: 512-dimension
        :param list_facial_vector:
        :return:user_id, name, min_distance closest
        """
        # Get list vector and search in database return face id and distance of each vector.
        match_identity = milvus_staging_dal.search_vector(list_facial_vector)
        user_id_of_group = []
        dis_follow_user_id = []
        name_follow_user_id = []
        for idx in range(len(match_identity)):
            if match_identity[idx]["distance"] < 0.6:
                name, url_match, user_id = identity_dal.find_identity_info_with_face_id_for_group(match_identity[idx]["id"])
                user_id_of_group.append(user_id)
                dis_follow_user_id.append(match_identity[idx]["distance"])
                name_follow_user_id.append(name)

        if len(user_id_of_group) > 0:
            count_name = Counter(user_id_of_group)
            user_id = list(count_name.keys())[0]
            name = name_follow_user_id[user_id_of_group.index(user_id)]
            min_distance = dis_follow_user_id[user_id_of_group.index(user_id)]
        else:
            user_id = "Unknown"
            name = "Unknown"
            if len(match_identity) > 0:
                min_distance = match_identity[0]["distance"]
            else:
                min_distance = None
        return user_id, name, min_distance

    def get_identity_list_facial_vector_v3(self, list_facial_vector):
        """
        Get list embedding vector of a group(can one vector), search in milvus , mongo
        and return a name closest matching with all vector; closest name is name have maximum number of vector match.
        Example: list_facial_vector = [[N], ...], N: 512-dimension
        :param list_facial_vector:
        :return:user_id, name, min_distance closest
        """
        # Get list vector and search in database return face id and distance of each vector.
        match_identity = []
        try:
            match_identity = milvus_staging_dal.search_vector(list_facial_vector)
        except Exception as e:
            print(e)
            print("Search in milvus failed.")
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        list_user_id = []
        dis_follow_user_id = []
        name_follow_user_id = []
        for idx in range(len(match_identity)):
            if match_identity[idx]["distance"] < 0.68:  # 0.6
                name, url_match, user_id = identity_dal.find_identity_info_with_face_id_for_group(match_identity[idx]["id"])
                list_user_id.append(user_id)
                dis_follow_user_id.append(match_identity[idx]["distance"])
                name_follow_user_id.append(name)
            else:
                list_user_id.append("Unknown")
                dis_follow_user_id.append(match_identity[idx]["distance"])
                name_follow_user_id.append("Unknown")

        return list_user_id, name_follow_user_id, dis_follow_user_id

    def detect_face_and_get_embedding_an_image_scrfd(self, image_rgb, det_threshold=0.5, video=False):
        """
        Take only one face in image.(for register identity and sign_in face)
        Takes an RGB image and detect face, get embedding of face.
        Will take face have size box biggest if an image have more than one face
        :param image_rgb: [height, width, 3]
        :param det_threshold: 0.6
        :return: facial_vector[512], face_array[height, width, 3]
        """
        start_time = time.time()
        box_detect, landmark_detect, accuracy_detect = self.detect_batch_img_array_scrfd([image_rgb], det_threshold=det_threshold)
        print("detect_batch_img_array_scrfd cost: ", time.time() - start_time)
        boxes_face = box_detect[0]
        landmark_detect = landmark_detect[0]  # batch = 1
        accuracy_detect = accuracy_detect[0]
        face_base64 = None
        image_face = None
        previous_area = 0
        accuracy_face_detect = 0
        for idx, box_face in enumerate(boxes_face):
            # Filter face register
            # 1. Select biggest area box face
            face_width, face_height = box_face[2] - box_face[0], box_face[3] - box_face[1]
            current_area = face_width * face_height
            if current_area < previous_area:
                continue
            previous_area = current_area

            # 2. Select min face-size(112x112)
            if face_width < 40 or face_height < 40:
                print("face_width, face_height < 40")
                continue

            # 3. Get is front face
            if video:
                start_time = time.time()
                roll_pitch_yaw = get_Roll_Pitch_Yaw_new(box_face, landmark_detect[idx], MIN_ROLL, MIN_PITCH, MIN_YAW)
                print("get_Roll_Pitch_Yaw_new cost: ", time.time() - start_time)
                # khong phai chinh dien > khong can lay vector embedding
                if not is_frontal_face(roll_pitch_yaw):
                    print("Not is_frontal_face")
                    continue

            face_base64, image_face = self.get_base64_box_face(box_face, image_rgb, align=True, landmark=np.array(landmark_detect[idx]))
            accuracy_face_detect = int(accuracy_detect[idx] * 100)
        if face_base64 is None:
            print("face_base64 is None")
            return None, None, None
        req = {"images": {"data": [face_base64]}, "embed_only": True}
        resp = requests.post(self.api_insightface, json=req)
        data = resp.json()
        facial_vector = data["data"][0]["vec"]

        return facial_vector, image_face, accuracy_face_detect

    def face_for_url_image(self, url):
        """
        get url image (minio) and return embeddings face
        :param url:
        :return: list embeddings [[N]], N = 512
        """
        img_array = read_url_img_to_array(url)
        facial_vector, image_face, accuracy_face_detect = self.detect_face_and_get_embedding_an_image_scrfd(img_array)
        return facial_vector, image_face


if __name__ == '__main__':
    arr_img = read_url_img_to_array("https://file.erp.clover.edu.vn/file-storage/2022/03/20220326/3a02d759-dd15-fe60-ea9e-1f3c2ca952a3.png")
    h, w, _ = arr_img.shape
    image_rgb = cv2.cvtColor(arr_img, cv2.COLOR_BGR2RGB)
    FaceLocalUtils().detect_face_and_get_embedding_an_image_scrfd(image_rgb)