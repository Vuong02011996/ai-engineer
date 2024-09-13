import cv2
import numpy as np
import requests
import time
from collections import Counter
import sys
import os

import torch

from app.app_utils.roll_pitch_yaw_utils import get_Roll_Pitch_Yaw_new, is_frontal_face
from app.mongo_dal.identity_dal import IdentityDAL
# from core.models_local.face_detection.DSFDPytorchInference import face_detection
from core.main.main_utils.box_utils import extend_bbox
from core.main.main_utils.draw import draw_det_when_track
from core.main.main_utils.helper import convert_np_array_to_base64, read_url_img_to_array,align_face
from app.milvus_dal.clover_dal import MilvusCloverDAL
# sys.path.append("../../core/main/yolov5_detect")
# from core.main.yolov5_detect.yolov5_detect_image import Y5Detect
# y5_model = Y5Detect(weights="../../core/main/yolov5_detect/model_head/y5headbody_v2.pt")


# Cái này là nguyên nhân GPU tăng lên mỗi khi start dù không dùng model trực tiếp.
# detector = face_detection.build_detector(
#     "RetinaNetMobileNetV1",  # RetinaNetResNet50, RetinaNetMobileNetV1
#     # max_resolution=200
# )

milvus_staging_dal = MilvusCloverDAL()
identity_dal = IdentityDAL()

# global variables
MIN_ROLL, MIN_PITCH, MIN_YAW = 90, 90, 90
port_model_insight = int(os.getenv("port_model_insight"))
ip_run_service_insight = os.getenv("ip_run_service_insight")

class FaceLocalUtils(object):
    def __init__(self, image_size_det=(1000, 1000), det_threshold=0.65, image_size_embedding=(112, 112),
                 distance_threshold=0.5):
        self.image_size_det = image_size_det
        self.det_threshold = det_threshold
        self.det_threshold_srcfd = 0.65
        self.image_size_embedding = image_size_embedding
        self.distance_threshold = distance_threshold
        # 18085 have detect mask
        self.api_insightface = "http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract"

    def get_base64_box_face(self, box_face, arr_img, align=True, landmark=None):
        box_face = list(map(int, box_face[:4]))
        image_face = arr_img[box_face[1]:box_face[3], box_face[0]:box_face[2]]

        # bbox = box_face
        # x_min, y_min, x_max, y_max = bbox
        # # Draw the bounding box on the image
        # cv2.rectangle(arr_img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Green color, thickness = 2
        # # Show the image with bounding box
        # cv2.imshow("Image with Bounding Box", arr_img)
        # cv2.waitKey(0)

        # cv2.imshow("Samed", image_face)
        # cv2.waitKey(0)
        if 0 in image_face.shape:
            # Take face error
            return None, None
        if align and landmark is not None:
            # image_face_resize = align_face(arr_img, box_face, landmark)
            image_face_resize = align_face(arr_img, box_face, np.array(landmark))
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
        print("ip_run_service_insight: ", ip_run_service_insight)
        resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
        data = resp.json()
        facial_vector = data["data"][0]["vec"]
        return facial_vector

    def detect_batch_img_array(self, list_img_array, resize=False):
        """
        :param list_img_array: list image array [[height, width, 3], [height, width, 3], ...]
        :param resize
        :return: result_detect(tuple 2) -
        result_detect[0](list B) is bbox [N, 5]
        result_detect[1](list B) is landmark [N, 5, 2]
        B: number of batch or len(list_img_array)
        N: number of box face in each image of batch.
        """
        batch_im = None
        for img_arr in list_img_array:
            if resize:
                img_arr = cv2.resize(img_arr, self.image_size_det, interpolation=cv2.INTER_AREA)
            if batch_im is None:
                batch_im = img_arr[None, :, :, :]
            else:
                # batch_im = np.concatenate((batch_im, im), axis=0)
                batch_im = np.vstack((batch_im, img_arr[None, :, :, :]))
        result_detect = detector.batched_detect_with_landmarks(batch_im)
        """Nếu out of memory cuda sẽ không reset bộ nhớ lại được 
        https://discuss.pytorch.org/t/out-of-memory-and-cant-release-gpu-memory/132601"""
        torch.cuda.empty_cache()

        # print(f"Detection time: {time.time() - t:.3f}")
        return result_detect[0], result_detect[1]

    def detect_batch_img_array_scrfd(self, list_img_array):
        target = []
        for img_arr in list_img_array:
            target.append(convert_np_array_to_base64(img_arr))

        req = {"images": {"data": target}, "threshold": self.det_threshold_srcfd, "return_landmarks": True, "embed_only": False,
               "extract_embedding": False}
        resp = requests.post(self.api_insightface, json=req)
        data = resp.json()
        box_detect = []
        landmark_detect = []
        accuracy_detect = []
        for faces_img in data["data"]:
            box_detect.append(list(map(lambda d: d['bbox'], faces_img['faces'])))
            landmark_detect.append(list(map(lambda d: d['landmarks'], faces_img['faces'])))
            accuracy_detect.append(list(map(lambda d: d['prob'], faces_img['faces'])))
            return box_detect, landmark_detect, accuracy_detect
        return None, None, None

    def detect_and_get_embedding_all_face_of_list_img_array(self, list_img_array, resize=True):
        """
        Get embedding, bbox face from list_img_array
        :param list_img_array: list numpy array [N, height, width, 3]
        :param resize
        :return: list embedding, list bbox face, list id image , all the same length, length is number of face in all image.
        """
        box_detect, landmark_detect = self.detect_batch_img_array(list_img_array, resize=resize)
        assert len(list_img_array) == len(box_detect)

        list_facial_vector_all_image = []
        list_image_face_all_image = []
        list_id_image = []

        for id_image in range(len(box_detect)):
            arr_img = list_img_array[id_image]
            w_scale = arr_img.shape[1] / self.image_size_det[0]
            h_scale = arr_img.shape[0] / self.image_size_det[1]

            boxes_face = box_detect[id_image]
            list_face_base64 = []
            for idx, box_face in enumerate(boxes_face):
                if box_face[-1] < self.det_threshold:
                    continue
                box_face[0] *= w_scale
                box_face[1] *= h_scale
                box_face[2] *= w_scale
                box_face[3] *= h_scale
                face_base64, image_face = self.get_base64_box_face(box_face, arr_img, align=True)
                if face_base64 is None:
                    continue
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
            if match_identity[idx]["distance"] < self.distance_threshold:
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

    def detect_face_and_get_embedding_an_image(self, image_rgb, resize=False):
        """
        Takes an RGB image and detect face, get embedding of face.
        Will take face have size box biggest if an image have more than one face
        :param image_rgb: [height, width, 3]
        :param resize: True or False
        :return: facial_vector[512], face_array[height, width, 3]
        """
        # box_detect, landmark_detect = self.detect_batch_img_array([image_rgb], resize=resize)
        box_detect, landmark_detect, accuracy_detect = self.detect_batch_img_array_scrfd([image_rgb])
        boxes_face = box_detect[0] # batch = 1
        landmark_detect = landmark_detect[0]
        accuracy_detect = accuracy_detect[0] # batch = 1

        #--------------------------------------------
        # bbox = boxes_face[0]
        # x_min, y_min, x_max, y_max = bbox
        # # Draw the bounding box on the image
        # cv2.rectangle(image_rgb, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Green color, thickness = 2
        # # Show the image with bounding box
        # cv2.imshow("Image with Bounding Box", image_rgb)
        # cv2.waitKey(0)
        # --------------------------------------------

        w_scale = h_scale = None
        if resize:
            w_scale = image_rgb.shape[1] / self.image_size_det[0]
            h_scale = image_rgb.shape[0] / self.image_size_det[1]
        face_base64 = None
        image_face = None
        previous_area = 0
        accuracy_face_detect = 0
        print("boxes_face: ", boxes_face)
        for idx, box_face in enumerate(boxes_face):
            # print("box_face[-1]", box_face[-1])
            if box_face[-1] < self.det_threshold:
                continue
            # Filter face register
            # 1. Select biggest area box face
            face_width, face_height = box_face[2] - box_face[0], box_face[3] - box_face[1]
            current_area = face_width * face_height
            if current_area < previous_area:
                continue
            previous_area = current_area

            # 2. Select min face-size(112x112)
            # if face_width < 112 or face_height < 112:
            #     continue

            if resize:
                box_face[0] *= w_scale
                box_face[1] *= h_scale
                box_face[2] *= w_scale
                box_face[3] *= h_scale
                for i, point in enumerate(landmark_detect[idx]):
                    landmark_detect[idx][i][0] *= w_scale
                    landmark_detect[idx][i][1] *= h_scale
            face_base64, image_face = self.get_base64_box_face(box_face, image_rgb, align=True, landmark=landmark_detect[idx])

            # accuracy_face_detect = int(box_face[-1] * 100)
            accuracy_face_detect = int(accuracy_detect[idx] * 100)
        # print("face_base64, image_face", face_base64, image_face)
        if face_base64 is None:
            return None, None, None
        req = {"images": {"data": [face_base64]}, "embed_only": True}
        resp = requests.post(self.api_insightface, json=req)
        data = resp.json()
        facial_vector = data["data"][0]["vec"]

        return facial_vector, image_face, accuracy_face_detect

    def detect_face_and_get_embedding_an_image_srcfc(self, image_rgb, resize=True):
        """
        Takes an RGB image and detect face, get embedding of face.
        Will take face have size box biggest if an image have more than one face
        :param image_rgb: [height, width, 3]
        :param resize: True or False
        :return: facial_vector[512], face_array[height, width, 3]
        """
        box_detect, landmark_detect, accuracy_detect = self.detect_batch_img_array_scrfd([image_rgb])
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
            if face_width < 112 or face_height < 112:
                continue

            # 3. Get is front face
            roll_pitch_yaw = get_Roll_Pitch_Yaw_new(box_face, landmark_detect[idx], MIN_ROLL, MIN_PITCH, MIN_YAW)
            # khong phai chinh dien > khong can lay vector embedding
            if not is_frontal_face(roll_pitch_yaw):
                continue

            face_base64, image_face = self.get_base64_box_face(box_face, image_rgb, align=True, landmark=np.array(landmark_detect[idx]))
            accuracy_face_detect = int(accuracy_detect[idx] * 100)
        if face_base64 is None:
            return None, None, None
        req = {"images": {"data": [face_base64]}, "embed_only": True}
        resp = requests.post(self.api_insightface, json=req)
        data = resp.json()
        facial_vector = data["data"][0]["vec"]

        return facial_vector, image_face, accuracy_face_detect

    @staticmethod
    def detect_face_bbox_head_batch(batch_im_head, x_offset, y_offset, w_scale, h_scale):
        boxes_face = np.zeros((batch_im_head.shape[0], 4), dtype=int)
        dets = detector.batched_detect_with_landmarks(batch_im_head)
        # one image head only one face
        for image_id in range(len(dets[0])):
            if len(dets[0][image_id]) > 0:
                box_face = dets[0][image_id][0]

                box_face[0] *= w_scale[image_id]
                box_face[1] *= h_scale[image_id]
                box_face[2] *= w_scale[image_id]
                box_face[3] *= h_scale[image_id]

                box_face[0] += x_offset[image_id]
                box_face[1] += y_offset[image_id]
                box_face[2] += x_offset[image_id]
                box_face[3] += y_offset[image_id]
                boxes_face[image_id] = list(map(int, box_face[:4]))
            else:
                boxes_face[image_id] = np.zeros(4, dtype=int)
        return boxes_face

    def detect_head_face_and_get_embedding_an_image(self, image_rgb):
        """
        Takes an RGB image and detect face, get embedding of face.
        Will take face have size box biggest if an image have more than one face
        :param image_rgb: [height, width, 3]
        :param resize: True or False
        :return: facial_vector[512], face_array[height, width, 3]
        """
        batch_image_head, x_offset, y_offset, w_scale, h_scale = get_batch_image_head(image_rgb)
        if batch_image_head is not None:
            boxes_face = self.detect_face_bbox_head_batch(batch_image_head, x_offset, y_offset, w_scale, h_scale)
        else:
            # Case no track_bbs_ids (no head, no track)
            boxes_face = []
        face_base64 = None
        image_face = None
        previous_area = 0
        for idx, box_face in enumerate(boxes_face):
            # if box_face[-1] < self.det_threshold:
            #     continue
            # Select biggest area box face
            face_width, face_height = box_face[2] - box_face[0], box_face[3] - box_face[1]
            current_area = face_width * face_height
            if current_area < previous_area:
                continue
            previous_area = current_area
            face_base64, image_face = self.get_base64_box_face(box_face, image_rgb)
        if face_base64 is None:
            return None, None
        req = {"images": {"data": [face_base64]}, "embed_only": True}

        port_model_insight = int(os.getenv("port_model_insight"))
        ip_run_service_insight = os.getenv("ip_run_service_insight")
        resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
        data = resp.json()
        facial_vector = data["data"][0]["vec"]

        return facial_vector, image_face

    def face_for_url_image(self, url):
        """
        get url image (minio) and return embeddings face
        :param url:
        :return: list embeddings [[N]], N = 512
        """
        img_array = read_url_img_to_array(url)
        facial_vector, image_face, accuracy_face_detect = self.detect_face_and_get_embedding_an_image(img_array)
        return facial_vector, image_face


def get_batch_image_head(image_rgb):
    # boxes, labels, scores = y5_model.predict(image_rgb, show=False)
    box_detect, landmark_detect = FaceLocalUtils().detect_batch_img_array([image_rgb], resize=False)
    print("box head", box_detect)
    boxes = box_detect[0]
    max_size_head = 200
    batch_image_head = None
    x_offset = []
    y_offset = []
    w_scale = []
    h_scale = []
    boxes_head = []

    for i, box in enumerate(boxes):
        box = list(map(int, box[:4]))
        box = extend_bbox(box, image_rgb.shape)
        image_head = image_rgb[box[1]:box[3], box[0]:box[2]]

        cv2.imwrite("/home/vuong/Desktop/Project/GG_Project/clover/Test/image/" + "file_" + str(np.random.randint(10000000)) + ".png", image_head)

        w_scale.append(image_head.shape[1] / max_size_head)
        h_scale.append(image_head.shape[0] / max_size_head)
        x_offset.append(box[0])
        y_offset.append(box[1])
        boxes_head.append(box)

        if 0 in image_head.shape:
            image_head = np.zeros((max_size_head, max_size_head, 3), dtype=int)
        else:
            image_head = cv2.resize(image_head, (max_size_head, max_size_head), interpolation=cv2.INTER_AREA)

        image_head = image_head[:, :, ::-1]
        if batch_image_head is None:
            batch_image_head = image_head[None, :, :, :]
        else:
            batch_image_head = np.vstack((batch_image_head, image_head[None, :, :, :]))

    return batch_image_head, x_offset, y_offset, w_scale, h_scale