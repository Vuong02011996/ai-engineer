"""
Using detect face using api from InsightFACE REST - API
"""
import traceback
from datetime import datetime
import json
import cv2
import pandas as pd
import time
import numpy as np
import pika
import os
import requests
from sentry_sdk import capture_message

from app.minio_dal.minio_client import upload_array_image_to_minio
from core.main.main_utils.box_utils import extend_bbox, extend_bbox_percent
from core.main.main_utils.helper import convert_np_array_to_base64


ip_rabbitMQ_server = os.getenv("ip_rabbitMQ_server")
port_rabbitMQ_server = int(os.getenv("port_rabbitMQ_server"))
FACE_RECOGNITION_EXCHANGES = "FACE_RECOGNITION_EXCHANGES"


def detect_face_bbox_head_v2(cam, head_bbox_queue, face_embedding_queue, port_model_insight, object_dal):
    url_face = "http://localhost:" + port_model_insight + "/extract"
    max_size_head = 224
    while cam.cap.isOpened():
        track_bbs_ids, frame_rgb, frame_count, boxes, scores = head_bbox_queue.get()
        x_offset = []
        y_offset = []
        target = []
        # Select boxes to model face detection
        # 1. Filter head have score good
        if len(track_bbs_ids) != len(scores):
            continue
        # print('******************track_bbs_ids********', track_bbs_ids)
        # print('******************scores********', scores)
        idx_score_choice = np.where(scores > 0.8)[0]
        # print('******************idx_score_choice********', idx_score_choice)
        track_bbs_ids = track_bbs_ids[idx_score_choice]

        # print('******************track_bbs_ids********', track_bbs_ids)

        # 2. track have name, no detect face
        '''
        track_bbs_ids******** [[ 422.01551343  241.06090725  462.96419502  287.93996043   86.        ]
                             [ 505.70197175  248.95640001  561.811004    310.68265708   85.        ]
                             [1100.56955249   35.0716653  1143.46088058   88.97226464   84.        ]
                             [ 331.26484193  696.92370378  443.59828949  814.54358437   83.        ]
                             [1566.67493231   78.67392203 1609.08514647  130.50748943   81.        ]
                             [ 665.83891558  354.76546971  740.55086234  438.24474874   70.        ]
                             [ 277.66729744  504.67188796  348.96768508  583.63799734   18.        ]
                             [1046.30002424  354.43839143 1128.73557428  458.63475103    8.        ]
                             [ 293.17633392  362.07356944  342.88229743  426.99782472    7.        ]
                             [1446.99744608  145.94994396 1497.99546336  212.06428614    6.        ]]
        '''
        object_data = object_dal.find_all_object_have_name_by_process_name(cam.process_name)
        if len(object_data) > 0:
            list_track_id = list(map(lambda x: x["track_id"], object_data))
            # print('******************list_track_id********', list_track_id)

            track_bbs_ids = track_bbs_ids[~np.isin(track_bbs_ids[:, -1], list_track_id)]

            # print('******************track_bbs_ids********', track_bbs_ids)

        for i, box in enumerate(track_bbs_ids):
            box = list(map(int, box[:4]))
            box = extend_bbox(box, frame_rgb.shape)
            image_head = frame_rgb[box[1]:box[3], box[0]:box[2]]
            x_offset.append(box[0])
            y_offset.append(box[1])

            if 0 in image_head.shape:
                image_head = np.zeros((max_size_head, max_size_head, 3), dtype=int)

            image_head = image_head[:, :, ::-1]
            target.append(convert_np_array_to_base64(image_head))
        # print("len(target)", len(target))

        start_time = time.time()
        if len(target) > 0:
            print('******************len target********', len(target))
            req = {"images": {"data": target}, "threshold": 0.65, "return_landmarks": True, "embed_only": False,
                   "extract_embedding": False}
            # start_time = time.time()
            resp = requests.post(url_face, json=req)
            # print("Reponse cost: ", time.time() - start_time)
            data = resp.json()
            boxes_face = np.zeros((len(target), 5))
            landmarks_face = np.zeros((len(target), 5, 2))
            for head_id, faces_img in enumerate(data["data"]):
                # if have face in image head
                if len(faces_img['faces']) > 0:
                    box_face = faces_img['faces'][0]['bbox']  # only take index 0 because one image head have one face
                    box_face[0] += x_offset[head_id]
                    box_face[1] += y_offset[head_id]
                    box_face[2] += x_offset[head_id]
                    box_face[3] += y_offset[head_id]
                    accuracy = faces_img['faces'][0]['prob']
                    box_face.append(accuracy)
                    landmark_detect = faces_img['faces'][0]['landmarks']

                    for i, point in enumerate(landmark_detect):
                        landmark_detect[i][0] += x_offset[head_id]
                        landmark_detect[i][1] += y_offset[head_id]

                    boxes_face[head_id] = box_face
                    landmarks_face[head_id] = landmark_detect
                else:
                    boxes_face[head_id] = np.zeros(5)
                    landmarks_face[head_id] = np.zeros((5, 2))
        else:
            # Case no track_bbs_ids (no head, no track)
            boxes_face = []
            landmarks_face = []

        # print("boxes_face: ", boxes_face)
        print("detect_face_bbox_head cost: ", time.time() - start_time)
        assert len(boxes_face) == len(track_bbs_ids) == len(landmarks_face)

        face_embedding_queue.put([boxes_face, landmarks_face, frame_rgb, track_bbs_ids, frame_count])

    cam.cap.release()


def detect_face_bbox_head_v1(cam, head_bbox_queue, face_embedding_queue, info_cam_running, object_dal):
    port_model_insight = info_cam_running["port_model_insight"] if info_cam_running.get("port_model_insight") is not None else '18081'
    ip_run_service_insight = info_cam_running["ip_run_service_insight"] if info_cam_running.get(
        "ip_run_service_insight") is not None else 'localhost'
    url_face = "http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract"
    # url_face = "http://api-face.oryza.vn" + "/extract"
    max_size_head = 224
    time_cost = []
    list_track_id_send = []
    while cam.cap.isOpened():
        track_bbs_ids, frame_, frame_count, boxes, scores = head_bbox_queue.get()
        frame_rgb = frame_.copy()
        track_ids = track_bbs_ids[:, -1]
        x_offset = []
        y_offset = []
        target = []
        # Select boxes to model face detection
        # 1. track have name, no detect face
        '''
        track_bbs_ids******** [[ 422.01551343  241.06090725  462.96419502  287.93996043   86.        ]
                             [ 505.70197175  248.95640001  561.811004    310.68265708   85.        ]
                             [1100.56955249   35.0716653  1143.46088058   88.97226464   84.        ]
                             [ 331.26484193  696.92370378  443.59828949  814.54358437   83.        ]
                             [1566.67493231   78.67392203 1609.08514647  130.50748943   81.        ]
                             [ 665.83891558  354.76546971  740.55086234  438.24474874   70.        ]
                             [ 277.66729744  504.67188796  348.96768508  583.63799734   18.        ]
                             [1046.30002424  354.43839143 1128.73557428  458.63475103    8.        ]
                             [ 293.17633392  362.07356944  342.88229743  426.99782472    7.        ]
                             [1446.99744608  145.94994396 1497.99546336  212.06428614    6.        ]]
        '''
        '''    + track have name, no detect face: xoa track khi track da co name(khong xu li face detect)'''
        object_data = object_dal.find_all_object_have_name_by_process_name(cam.process_name)
        if len(object_data) > 0:
            list_track_id = list(map(lambda x: x["track_id"], object_data))
            # print('******************list_track_id********', list_track_id)
            track_bbs_ids = track_bbs_ids[~np.isin(track_bbs_ids[:, -1], list_track_id)]
            '''--------------end-------------------------------'''

        # 2. Filter head have score good
        # if len(track_bbs_ids) > 5 and len(track_bbs_ids) == len(scores):
        #     # print('******************track_bbs_ids********', track_bbs_ids)
        #     # print('******************scores********', scores)
        #     # idx_score_choice = np.where(scores > 0.3)[0]
        #     # print('******************idx_score_choice********', idx_score_choice)
        #     # track_bbs_ids = track_bbs_ids[idx_score_choice]
        #     track_bbs_ids = track_bbs_ids[:5]

        # print('******************track_bbs_ids********', track_bbs_ids)
        list_image_heads = []
        for i, box in enumerate(track_bbs_ids):
            box = list(map(int, box[:4]))
            frame_ = frame_rgb.copy()
            box = extend_bbox(box, frame_.shape)
            image_head = frame_[box[1]:box[3], box[0]:box[2]]
            x_offset.append(box[0])
            y_offset.append(box[1])

            if 0 in image_head.shape:
                image_head = np.zeros((max_size_head, max_size_head, 3), dtype=int)

            image_head = image_head[:, :, ::-1]
            # cv2.imwrite(f"/home/oryza/Desktop/test_image/image_{frame_count}_{i}.png", image_head)

            target.append(convert_np_array_to_base64(image_head))
            list_image_heads.append(image_head)
        # print("len(target)", len(target))
        boxes_face = []
        landmarks_face = []

        start_time = time.time()
        if len(target) > 0:
            # print('******************len target********', len(target))
            req = {"images": {"data": target}, "threshold": 0.65, "return_landmarks": True, "embed_only": False,
                   "extract_embedding": False}
            # start_time = time.time()
            try:
                resp = requests.post(url_face, json=req)
                # print("Reponse cost: ", time.time() - start_time)
                # time_cost.append(time.time() - start_time)
                data = resp.json()
            except Exception as e:
                print(e)
                data = {}
                data["data"] = []

            boxes_face = np.zeros((len(target), 5))
            landmarks_face = np.zeros((len(target), 5, 2))
            for head_id, faces_img in enumerate(data["data"]):
                # if have face in image head
                if len(faces_img['faces']) > 0:
                    box_face = faces_img['faces'][0]['bbox']  # only take index 0 because one image head have one face
                    # check face with image
                    # image_head_with_face = list_image_heads[head_id][box_face[1]:box_face[3], box_face[0]:box_face[2]]
                    # cv2.imwrite(f"/home/oryza/Desktop/test_image/image_{frame_count}_{head_id}_face.png", image_head_with_face)

                    box_face[0] += x_offset[head_id]
                    box_face[1] += y_offset[head_id]
                    box_face[2] += x_offset[head_id]
                    box_face[3] += y_offset[head_id]
                    accuracy = faces_img['faces'][0]['prob']
                    box_face.append(accuracy)
                    landmark_detect = faces_img['faces'][0]['landmarks']

                    for i, point in enumerate(landmark_detect):
                        landmark_detect[i][0] += x_offset[head_id]
                        landmark_detect[i][1] += y_offset[head_id]

                    boxes_face[head_id] = box_face
                    landmarks_face[head_id] = landmark_detect
                else:
                    boxes_face[head_id] = np.zeros(5)
                    landmarks_face[head_id] = np.zeros((5, 2))
        else:
            # Case no track_bbs_ids (no head, no track)
            boxes_face = []
            landmarks_face = []

        # print("boxes_face: ", boxes_face)
        time_head_cost = time.time() - start_time
        if time_head_cost > 0.05:
            print("face detect cost: ", time_head_cost)
        # print("len(boxes_face), len(track_bbs_ids), len(landmarks_face)", len(boxes_face), len(track_bbs_ids), len(landmarks_face))
        assert len(boxes_face) == len(track_bbs_ids) == len(landmarks_face)
        face_embedding_queue.put([boxes_face, landmarks_face, frame_rgb, track_bbs_ids, frame_count])

    cam.cap.release()

    # df = pd.DataFrame(np.array(time_cost), columns=['Values'])
    # # Save DataFrame to text file
    # df.to_csv('/home/oryza/Desktop/Projects/Face_Detection/data_test/time_cost_face_detect' + cam.process_name + '.txt', index=False)


if __name__ == '__main__':
    pass