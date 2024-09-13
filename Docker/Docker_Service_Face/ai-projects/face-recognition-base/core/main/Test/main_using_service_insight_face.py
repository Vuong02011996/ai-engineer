import cv2
import sys
import base64
import requests
from queue import Queue
import time
from kthread import KThread
import numpy as np
import os
from core.main.mot_tracking.mot_sort_tracker import Sort
from core.main.mot_tracking import untils_track
from core.main.main_utils.box_utils import extend_bbox

sys.path.append("../face_detect/pytorch_retinaface/DSFDPytorchInference")

sys.path.append("../../models_local/head_detection/yolov5_detect")
from core.models_local.head_detection.yolov5_detect.yolov5_detect_image import Y5Detect
from core.main.main_utils.draw import draw_boxes_tracking, draw_det_when_track, draw_single_pose, draw_data_action, \
    draw_region, draw_boxes_one_track_id


y5_model = Y5Detect(weights="../../../core/models_local/head_detection/yolov5_detect/model_head/y5headbody_v2.pt")
class_names = y5_model.class_names
mot_tracker = Sort(class_names)
path_save_bbox = "/core/main/face_detect/image_head/"


class InfoCam(object):
    def __init__(self, cam_name):
        self.cap = cv2.VideoCapture(cam_name)
        self.frame_start = 0
        self.total_frame_video = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps_video = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def video_capture(cam, frame_detect_queue, frame_origin_queue):
    frame_count = cam.frame_start

    cam.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    while cam.cap.isOpened():
        start_time = time.time()
        ret, frame_ori = cam.cap.read()
        # time.sleep(0.01)
        if not ret:
            break
        image_rgb = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2RGB)

        print("##################################")
        print("video_capture cost", time.time() - start_time)
        if frame_detect_queue.full() is False:
            frame_detect_queue.put([image_rgb, frame_ori, frame_count])
            frame_origin_queue.put([frame_ori, frame_count])
        else:
            time.sleep(0.001)
        # print("frame_count: ", frame_count)

        if frame_count == 298:
            a = 0
        frame_count += 1

    cam.cap.release()


def head_detect(cam, frame_detect_queue, detections_queue):
    while cam.cap.isOpened():
        if frame_detect_queue.empty() is False:
            image_rgb, frame_ori, frame_count = frame_detect_queue.get()
            start_time = time.time()
            boxes, labels, scores, detections_sort = y5_model.predict_sort(image_rgb, label_select=["head"])
            # for i in range(len(scores)):
            #     detections_tracking = bboxes[i].append(scores[i])
            print("head_detect cost: ", time.time() - start_time)
            if detections_queue.full() is False:
                detections_queue.put([boxes, labels, scores, image_rgb, detections_sort, frame_ori, frame_count])
            else:
                time.sleep(0.001)
        else:
            time.sleep(0.001)

    cam.cap.release()


def bbox2points(bbox):
    """
    From bounding box yolo format
    to corner points cv2 rectangle
    """
    x, y, w, h = bbox
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def to_tlwh(tlbr):
    """Convert bounding box to format `(min x, min y, max x, max y)`, i.e.,
    `(top left, bottom right)`.
    """
    ret = tlbr.copy()
    # ret[2:] += ret[:2]
    box = []
    for bbox in ret:
        w = int(bbox[2]) - int(bbox[0])
        h = int(bbox[3]) - int(bbox[1])
        box.append([int(bbox[0]) + w/2, int(bbox[1]) + h/2, w, h])
    return box


def tracking(cam, detections_queue, tracking_queue, head_bbox_queue):
    """
    :param cam:
    :param head_bbox_queue:
    :param detections_queue:
    :param tracking_queue:
    :return:
    Tracking using SORT. Hungary + Kalman Filter.
    Using mot_tracker.update()
    Input: detections [[x1,y1,x2,y2,score,label],[x1,y1,x2,y2,score, label],...], use np.empty((0, 5)) for frames without detections
    Output: [[x1,y1,x2,y2,id1, label],[x1,y1,x2,y2,id2, label],...]
    """
    region_track = np.array([[0, 0],
                             [cam.width, 0],
                             [cam.width, cam.height],
                             [0, cam.height]])

    while cam.cap.isOpened():
        if detections_queue.empty() is False:
            boxes, labels, scores, image_rgb, detections_sort, frame_ori, frame_count = detections_queue.get()

            start_time = time.time()
            if len(boxes) == 0:
                detections = np.empty((0, 6))
            else:
                detections = detections_sort
                # check and select the detection is inside region tracking
                detections, list_idx_bbox_del, list_idx_bbox_remain = untils_track.select_bbox_inside_polygon(detections, region_track)

            track_bbs_ids, unm_trk_ext = mot_tracker.update(detections, image=image_rgb)

            # check and select the track is inside region tracking
            track_bbs_ids, ist_idx_bbox_del, list_idx_bbox_remain = untils_track.select_bbox_inside_polygon(track_bbs_ids, region_track)
            unm_trk_ext, ist_idx_bbox_del, list_idx_bbox_remain = untils_track.select_bbox_inside_polygon(unm_trk_ext, region_track)
            print("tracking cost: ", time.time() - start_time)

            if tracking_queue.full() is False:
                head_bbox_queue.put([track_bbs_ids, frame_ori, frame_count])
                tracking_queue.put([track_bbs_ids, boxes, labels, scores, unm_trk_ext])
            else:
                time.sleep(0.001)
        else:
            time.sleep(0.001)

    cam.cap.release()


def save_bbox_head(image, boxes, frame_count, path):
    for i, box in enumerate(boxes):
        box = extend_bbox(box, image.shape)
        image_head = image[box[1]:box[3], box[0]:box[2]]
        cv2.imwrite(path + "head_" + str(frame_count) + "_" + str(i) + ".png", image_head)


def detect_face_bbox_head(cam, head_bbox_queue, face_detect_queue, face_embedding_queue):
    max_size_head = 200
    while cam.cap.isOpened():
        if head_bbox_queue.empty() is False:
            track_bbs_ids, frame_ori, frame_count = head_bbox_queue.get()
            x_offset = []
            y_offset = []
            w_scale = []
            h_scale = []
            list_head_base64 = []
            for i, box in enumerate(track_bbs_ids):
                box = list(map(int, box[:4]))
                box = extend_bbox(box, frame_ori.shape)
                image_head = frame_ori[box[1]:box[3], box[0]:box[2]]

                w_scale.append(image_head.shape[1] / max_size_head)
                h_scale.append(image_head.shape[0] / max_size_head)
                x_offset.append(box[0])
                y_offset.append(box[1])

                if 0 in image_head.shape:
                    image_head = np.zeros((max_size_head, max_size_head, 3), dtype=int)
                else:
                    success, encoded_image = cv2.imencode('.png', image_head)
                    image_face = encoded_image.tobytes()
                    head_base64 = base64.b64encode(image_face).decode('ascii')
                    list_head_base64.append(head_base64)

                # image_head = image_head[:, :, ::-1]
                # if batch_im is None:
                #     batch_im = image_head[None, :, :, :]
                # else:
                #     batch_im = np.vstack((batch_im, image_head[None, :, :, :]))

            start_time = time.time()
            # boxes_face = detect_face_bbox_head_batch(batch_im, x_offset, y_offset, w_scale, h_scale)
            req = {"images": {"data": list_head_base64},
                   "extract_embedding": False, "max_size": [max_size_head, max_size_head]}
            port_model_insight = int(os.getenv("port_model_insight"))
            ip_run_service_insight = os.getenv("ip_run_service_insight")
            resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
            data = resp.json()
            print("Response face cost: ", time.time() - start_time)
            if len(data["data"]) > 0:
                a = 0

            # print("boxes_face: ", boxes_face)
            # print("detect_face_bbox_head cost: ", time.time() - start_time)
            #
            boxes_face = [[]]
            if face_detect_queue.full() is False:
                face_detect_queue.put(boxes_face)
                face_embedding_queue.put([boxes_face, frame_ori])
            else:
                time.sleep(0.001)
        else:
            time.sleep(0.001)

    cam.cap.release()


def get_face_features(cam, face_embedding_queue):
    while cam.cap.isOpened():
        if face_embedding_queue.empty() is False:
            boxes_face, frame_ori = face_embedding_queue.get()
            face_embeddings = np.zeros((len(boxes_face), 512))
            list_face_base64 = []
            start_time = time.time()
            for idx, box_face in enumerate(boxes_face):
                if np.sum(box_face) == 0:
                    face_embedding = []
                else:
                    image_face = frame_ori[box_face[1]:box_face[3], box_face[0]:box_face[2]]
                    image_face = cv2.resize(image_face, (112, 112), interpolation=cv2.INTER_AREA)
                    image_face = cv2.cvtColor(image_face, cv2.COLOR_BGR2RGB)
                    success, encoded_image = cv2.imencode('.png', image_face)
                    image_face = encoded_image.tobytes()
                    face_base64 = base64.b64encode(image_face).decode('ascii')
                    list_face_base64.append(face_base64)
            req = {"images": {"data": list_face_base64}, "embed_only": True}
            port_model_insight = int(os.getenv("port_model_insight"))
            ip_run_service_insight = os.getenv("ip_run_service_insight")
            resp = requests.post("http://" + ip_run_service_insight + ":" + str(port_model_insight) + "/extract", json=req)
            data = resp.json()
            print("Response embedding cost: ", time.time() - start_time)
        else:
            time.sleep(0.001)

    cam.cap.release()


def drawing(cam, tracking_queue, frame_origin_queue, face_detect_queue, frame_final_queue, show_det=True):
    show_face = False
    while cam.cap.isOpened():
        if frame_origin_queue.empty() is False and tracking_queue.empty() is False:
            frame_origin, frame_count = frame_origin_queue.get()
            track_bbs_ids, boxes, labels, scores, unm_trk_ext = tracking_queue.get()
            boxes_face = face_detect_queue.get()

            start_time = time.time()
            # Save bounding box head with extend size
            # if len(boxes) > 0:
                # save_bbox_head(frame_origin, boxes, frame_count, path_save_bbox)
                # KThread(target=save_bbox_head, args=(frame_origin, boxes, frame_count, path_save_bbox)).start()

            if frame_origin is not None:
                if show_face:
                    image = draw_boxes_tracking(frame_origin, track_bbs_ids, boxes_face, track_bbs_ext=unm_trk_ext)
                else:
                    image = draw_boxes_tracking(frame_origin, track_bbs_ids, boxes_face=None, track_bbs_ext=unm_trk_ext)
                if show_det:
                    image = draw_det_when_track(frame_origin, boxes, scores=scores, labels=labels,
                                                class_names=class_names)
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                print("drawing cost", time.time() - start_time)
                print("##################################")
                if frame_final_queue.full() is False:
                    frame_final_queue.put([image, frame_count])
                else:
                    time.sleep(0.001)
        else:
            time.sleep(0.001)
    cam.cap.release()


def save_debug_image(frame_count, image):
    cv2.imwrite("/home/vuong/Desktop/Project/GG_Project/green-clover-montessori/new_core/debug_image/test_" + str(
        frame_count) + ".png", image)


def main():
    start_time = time.time()
    frame_detect_queue = Queue(maxsize=1)
    frame_origin_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    tracking_queue = Queue(maxsize=1)
    frame_final_queue = Queue(maxsize=1)
    face_detect_queue = Queue(maxsize=1)
    face_embedding_queue = Queue(maxsize=1)
    head_bbox_queue = Queue(maxsize=1)
    # input_path = "/home/vuong/Desktop/Data/Clover/Video diem danh/diem_danh_deo_khau_trang2.mp4"
    input_path = "/home/oryza/Videos/video_test_face.mp4"
    cam = InfoCam(input_path)

    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue, frame_origin_queue))
    thread2 = KThread(target=head_detect, args=(cam, frame_detect_queue, detections_queue))
    thread3 = KThread(target=tracking, args=(cam, detections_queue, tracking_queue, head_bbox_queue))
    thread4 = KThread(target=detect_face_bbox_head, args=(cam, head_bbox_queue, face_detect_queue, face_embedding_queue))
    thread5 = KThread(target=get_face_features, args=(cam, face_embedding_queue))
    thread6 = KThread(target=drawing, args=(cam, tracking_queue, frame_origin_queue, face_detect_queue, frame_final_queue))

    thread_manager = []
    thread1.daemon = True  # sẽ chặn chương trình chính thoát khi thread còn sống.
    thread1.start()
    thread_manager.append(thread1)
    thread2.daemon = True
    thread2.start()
    thread_manager.append(thread2)
    thread3.daemon = True
    thread3.start()
    thread_manager.append(thread3)
    thread4.daemon = True
    thread4.start()
    thread_manager.append(thread4)
    thread5.daemon = True
    thread5.start()
    thread_manager.append(thread5)
    thread6.daemon = True
    thread6.start()
    thread_manager.append(thread6)

    while cam.cap.isOpened():
        # cv2.namedWindow('output')
        if frame_final_queue.empty() is False:
            image, frame_count = frame_final_queue.get()
            image = cv2.resize(image, (1400, 640))
            cv2.imshow('output', image)
            # if frame_count >= 3000 and (frame_count <= 3500):
            #     KThread(target=save_debug_image, args=(frame_count, image)).start()
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyWindow('output')
                break
        else:
            time.sleep(0.001)

    for t in thread_manager:
        if t.is_alive():
            t.terminate()
    cv2.destroyAllWindows()
    total_time = time.time() - start_time
    print("FPS video: ", cam.fps_video)
    print("Total time: {}, Total frame: {}, FPS all process : {}".format(total_time, cam.total_frame_video,
                                                                         1/(total_time/cam.total_frame_video)), )


if __name__ == '__main__':
    main()

