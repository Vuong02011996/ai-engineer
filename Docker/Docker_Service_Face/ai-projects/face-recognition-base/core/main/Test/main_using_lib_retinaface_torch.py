import cv2
from queue import Queue
import time
from kthread import KThread
import numpy as np

from core.main.main_utils.box_utils import extend_bbox
from core.main.mot_tracking.mot_sort_tracker import Sort
from core.main.mot_tracking import untils_track
import face_detect.test_lib_retinaface_pytorch as face_detect

import sys
sys.path.append("../../models_local/head_detection/yolov5_detect")
from core.models_local.head_detection.yolov5_detect import Y5Detect, draw_boxes_tracking, draw_det_when_track


y5_model = Y5Detect(weights="../../core/main/yolov5_detect/model_head/y5headbody_v2.pt")
class_names = y5_model.class_names
mot_tracker = Sort(class_names)
path_save_bbox = "/core/main/face_detect/image_head/"
path_save_bbox_face = "/core/main/face_detect/image_face/"


class InfoCam(object):
    def __init__(self, cam_name):
        self.cap = cv2.VideoCapture(cam_name)
        self.frame_start = 0


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
                             [2560, 0],
                             [2560, 1440],
                             [0, 1440]])

    while cam.cap.isOpened():
        if detections_queue.empty() is False:
            boxes, labels, scores, image_rgb, detections_sort, frame_ori, frame_count = detections_queue.get()

            start_time = time.time()
            if len(boxes) == 0:
                detections = np.empty((0, 6))
            else:
                detections = detections_sort
                # check and select the detection is inside region tracking
                detections = untils_track.select_bbox_inside_polygon(detections, region_track)

            track_bbs_ids, unm_trk_ext = mot_tracker.update(detections, image=image_rgb)

            # check and select the track is inside region tracking
            track_bbs_ids = untils_track.select_bbox_inside_polygon(track_bbs_ids, region_track)
            unm_trk_ext = untils_track.select_bbox_inside_polygon(unm_trk_ext, region_track)
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
        # box = extend_bbox(box, image.shape)
        if 0 in box:
            continue
        image_save = image[box[1]:box[3], box[0]:box[2]]
        image_save = cv2.resize(image_save, (112, 112), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path + "head_" + str(frame_count) + "_" + str(i) + ".png", image_save)


def detect_face_bbox_head(cam, head_bbox_queue, face_detect_queue):
    while cam.cap.isOpened():
        if head_bbox_queue.empty() is False:
            track_bbs_ids, frame_ori, frame_count = head_bbox_queue.get()
            boxes_face = np.zeros((len(track_bbs_ids), 4), dtype=int)
            # if frame_count % 2 == 0:
            start_time = time.time()
            for i, box in enumerate(track_bbs_ids):
                box = list(map(int, box[:4]))
                box = extend_bbox(box, frame_ori.shape)
                image_head = frame_ori[box[1]:box[3], box[0]:box[2]]
                if 0 in image_head.shape:
                    box_face = np.zeros(4, dtype=int)
                else:
                    box_face = face_detect.predict_face_image_head(image_head)
                if len(box_face) > 0:
                    box_face[0] += box[0]
                    box_face[1] += box[1]
                    box_face[2] += box[0]
                    box_face[3] += box[1]
                else:
                    box_face = np.zeros(4, dtype=int)
                boxes_face[i] = box_face
            save_bbox_head(frame_ori, boxes_face, frame_count, path_save_bbox_face)
            print("detect_face_bbox_head cost: ", time.time() - start_time)
            if face_detect_queue.full() is False:
                face_detect_queue.put(boxes_face)
            else:
                time.sleep(0.001)
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
    frame_detect_queue = Queue(maxsize=1)
    frame_origin_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    tracking_queue = Queue(maxsize=1)
    frame_final_queue = Queue(maxsize=1)
    face_detect_queue = Queue(maxsize=1)
    head_bbox_queue = Queue(maxsize=1)
    # input_path = "/home/vuong/crop4.mp4"
    input_path = "/home/vuong/Desktop/Data/Clover/Video diem danh/diem_danh_deo_khau_trang2.mp4"
    cam = InfoCam(input_path)

    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue, frame_origin_queue))
    thread2 = KThread(target=head_detect, args=(cam, frame_detect_queue, detections_queue))
    thread3 = KThread(target=tracking, args=(cam, detections_queue, tracking_queue, head_bbox_queue))
    thread4 = KThread(target=detect_face_bbox_head, args=(cam, head_bbox_queue, face_detect_queue))
    thread5 = KThread(target=drawing, args=(cam, tracking_queue, frame_origin_queue, face_detect_queue, frame_final_queue))

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


if __name__ == '__main__':
    main()

