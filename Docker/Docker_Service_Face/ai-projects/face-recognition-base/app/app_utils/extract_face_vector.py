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


class ExtractVector(object):
    def __init__(self, image_size_det=(1000, 1000), det_threshold=0.65, image_size_embedding=(112, 112),
                 distance_threshold=0.5):
        self.image_size_det = image_size_det
        self.det_threshold = det_threshold
        self.det_threshold_srcfd = 0.65
        self.image_size_embedding = image_size_embedding
        self.distance_threshold = distance_threshold
        # 18085 have detect mask
        port_model_insight = int(os.getenv("port_model_insight"))
        ip_run_service_insight = os.getenv("ip_run_service_insight")
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

