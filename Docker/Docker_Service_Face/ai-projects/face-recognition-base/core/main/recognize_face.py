import time
import numpy as np
import cv2
import requests
import pandas as pd
from core.main.main_utils.helper import convert_np_array_to_base64, align_face


def get_face_features(cam, face_embedding_queue, matching_queue, info_cam_running):
    port_model_insight = info_cam_running["port_model_insight"] if info_cam_running.get(
        "port_model_insight") is not None else '18081'
    ip_run_service_insight = info_cam_running["ip_run_service_insight"] if info_cam_running.get(
        "ip_run_service_insight") is not None else 'localhost'
    url_face = "http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract"
    print("url_face: ", url_face)
    # url_face = "http://api-face.oryza.vn" + "/extract"
    align = True
    # time_cost = []
    while cam.cap.isOpened():
        boxes_face, landmarks_face, frame_, track_bbs_ids, frame_count = face_embedding_queue.get()
        frame_rgb = frame_.copy()
        face_embeddings = np.zeros((len(boxes_face), 512))
        list_face_base64 = []
        start_time = time.time()
        index_have_face = []
        for idx, box_face in enumerate(boxes_face):
            box_face = list(map(int, box_face[:4]))
            if np.sum(box_face) == 0:
                continue
            else:
                image_face = frame_rgb[box_face[1]:box_face[3], box_face[0]:box_face[2]]
                if align:
                    image_face = align_face(frame_rgb, box_face, landmarks_face[idx])
                else:
                    image_face = cv2.resize(image_face, (112, 112), interpolation=cv2.INTER_AREA)
                face_base64 = convert_np_array_to_base64(image_face)
                list_face_base64.append(face_base64)
                index_have_face.append(idx)
        if len(list_face_base64) > 0:
            req = {"images": {"data": list_face_base64}, "embed_only": True}
            resp = requests.post(url_face, json=req)
            data = resp.json()
            for idx in range(len(data["data"])):
                face_embeddings[index_have_face[idx]] = data["data"][idx]["vec"]

        assert len(track_bbs_ids) == face_embeddings.shape[0] == len(boxes_face)
        time_head_cost = time.time() - start_time
        if time_head_cost > 0.05:
            print("time extract cost: ", time_head_cost)
        # print("extract embedding cost: ", time.time() - start_time)
        # time_cost.append(time.time() - start_time)

        matching_queue.put([face_embeddings, track_bbs_ids, frame_count, frame_rgb, boxes_face, landmarks_face])
        # matching_queue.put([frame_rgb, frame_count])
        # print(face_embeddings, track_bbs_ids, frame_count, frame_rgb, boxes_face)

    cam.cap.release()
    # df = pd.DataFrame(np.array(time_cost), columns=['Values'])
    # # Save DataFrame to text file
    # df.to_csv('/home/oryza/Desktop/Projects/Face_Detection/data_test/time_cost_face_extract' + cam.process_name +'.txt', index=False)


if __name__ == '__main__':
    pass