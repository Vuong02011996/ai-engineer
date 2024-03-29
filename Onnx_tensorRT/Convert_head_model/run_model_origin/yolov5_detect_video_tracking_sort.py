import cv2
from queue import Queue

from Onnx_tensorRT.Convert_head_model.run_model_origin.my_utils import extend_bbox
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import Y5Detect
from Onnx_tensorRT.Convert_head_model.run_model_origin.my_utils import draw_boxes_tracking, draw_det_when_track
import time
from kthread import KThread
import numpy as np
from Onnx_tensorRT.Convert_head_model.run_model_origin.mot_tracking.mot_sort_tracker import Sort
from Onnx_tensorRT.Convert_head_model.run_model_origin.mot_tracking import untils_track

y5_model = Y5Detect(
    weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt")

class_names = y5_model.class_names
mot_tracker = Sort(class_names)
path_save_bbox = "/core/main/face_detect/image_head/"


class InfoCam(object):
    def __init__(self, cam_name):
        self.cap = cv2.VideoCapture(cam_name)
        self.frame_start = 0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.region_track = np.array([[0, 0],
                                 [self.width, 0],
                                 [self.width, self.height],
                                 [0, self.height]])


def video_capture(cam, frame_detect_queue, frame_origin_queue):
    frame_count = cam.frame_start

    cam.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    while cam.cap.isOpened():
        ret, frame_ori = cam.cap.read()
        # time.sleep(0.01)
        if not ret:
            break
        image_rgb = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2RGB)
        frame_detect_queue.put(image_rgb)
        frame_origin_queue.put([frame_ori, frame_count])
        print("frame_count: ", frame_count)
        frame_count += 1

    cam.cap.release()


def inference(cam, frame_detect_queue, detections_queue): #, tracking_queue):
    while cam.cap.isOpened():
        image_rgb = frame_detect_queue.get()
        boxes, labels, scores, detections_sort = y5_model.predict_sort(image_rgb, label_select=["head"])
        # for i in range(len(scores)):
        #     detections_tracking = bboxes[i].append(scores[i])
        detections_queue.put([boxes, labels, scores, image_rgb, detections_sort])
        # tracking_queue.put([detections_tracking])

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


def tracking(cam, frame_origin_queue, detections_queue, tracking_queue):
    """
    :param cam:
    :param frame_origin_queue:
    :param detections_queue:
    :param tracking_queue:
    :return:
    Tracking using SORT. Hungary + Kalman Filter.
    Using mot_tracker.update()
    Input: detections [[x1,y1,x2,y2,score,label],[x1,y1,x2,y2,score, label],...], use np.empty((0, 5)) for frames without detections
    Output: [[x1,y1,x2,y2,id1, label],[x1,y1,x2,y2,id2, label],...]
    """

    while cam.cap.isOpened():
        boxes, labels, scores, image_rgb, detections_sort = detections_queue.get()
        if len(boxes) == 0:
            detections = np.empty((0, 5))
        else:
            detections = detections_sort
            # check and select the detection is inside region tracking
            detections, list_idx_bbox_del, list_idx_bbox_remain = untils_track.select_bbox_inside_polygon(detections, cam.region_track)

        track_bbs_ids, unm_trk_ext = mot_tracker.update(detections, image=image_rgb)

        # check and select the track is inside region tracking
        track_bbs_ids, ist_idx_bbox_del, list_idx_bbox_remain = untils_track.select_bbox_inside_polygon(track_bbs_ids,
                                                                                                        cam.region_track)
        unm_trk_ext, ist_idx_bbox_del, list_idx_bbox_remain = untils_track.select_bbox_inside_polygon(unm_trk_ext,
                                                                                                      cam.region_track)
        # print("labels, scores", labels, scores)
        # print(track_bbs_ids)
        tracking_queue.put([track_bbs_ids, boxes, labels, scores, unm_trk_ext])

    cam.cap.release()


def save_bbox_head(image, boxes, frame_count, path):
    for i, box in enumerate(boxes):
        box = extend_bbox(box, image.shape)
        image_head = image[box[1]:box[3], box[0]:box[2]]
        cv2.imwrite(path + "head_" + str(frame_count) + "_" + str(i) + ".png", image_head)


def drawing(cam, tracking_queue, frame_origin_queue, frame_final_queue, show_det=True):
    while cam.cap.isOpened():
        frame_origin, frame_count = frame_origin_queue.get()
        track_bbs_ids, boxes, labels, scores, unm_trk_ext = tracking_queue.get()

        # Save bounding box head with extend size
        if len(boxes) > 0:
            save_bbox_head(frame_origin, boxes, frame_count, path_save_bbox)
            # KThread(target=save_bbox_head, args=(frame_origin, boxes, frame_count, path_save_bbox)).start()

        '''----------------------Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''
        track_bbs_ids, list_idx_bbox_del = untils_track.select_bbox_inside_many_resions(track_bbs_ids, cam.region_track)
        '''----------------------End Lọc track_bbs_ids nằm ngoài vùng config-------------------------'''

        if frame_origin is not None:
            image = draw_boxes_tracking(frame_origin, track_bbs_ids, boxes_face=None, track_bbs_ext=unm_trk_ext)
            if show_det:
                image = draw_det_when_track(frame_origin, boxes, scores=scores, labels=labels,
                                            class_names=class_names)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if frame_final_queue.full() is False:
                frame_final_queue.put([image, frame_count])
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
    input_path = "/home/oryza/Videos/video_test_face.mp4"
    cam = InfoCam(input_path)

    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue, frame_origin_queue))
    thread2 = KThread(target=inference, args=(cam, frame_detect_queue, detections_queue))
    thread3 = KThread(target=tracking, args=(cam, frame_origin_queue, detections_queue, tracking_queue))
    thread4 = KThread(target=drawing, args=(cam, tracking_queue, frame_origin_queue, frame_final_queue))

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

    while cam.cap.isOpened():
        # cv2.namedWindow('output')
        image, frame_count = frame_final_queue.get()
        image = cv2.resize(image, (1400, 640))
        cv2.imshow('output', image)
        if frame_count >= 3000 and (frame_count <= 3500):
            KThread(target=save_debug_image, args=(frame_count, image)).start()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyWindow('output')
            break

    for t in thread_manager:
        if t.is_alive():
            t.terminate()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

