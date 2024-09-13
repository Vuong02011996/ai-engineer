import cv2
from queue import Queue
from core.models_local.head_detection.yolov5_detect import Y5Detect
from core.main.main_utils.draw import draw_det_when_track
import time
from kthread import KThread
from core.main.mot_tracking.mot_sort_tracker import Sort

y5_model = Y5Detect(weights="../../../core/main/yolov5_detect/model_head/y5headbody_v2.pt")
class_names = y5_model.class_names
mot_tracker = Sort(class_names)
path_save_bbox = "/core/main/face_detect/image_head/"


class InfoCam(object):
    def __init__(self, cam_name):
        self.cap = cv2.VideoCapture(cam_name)
        self.frame_start = 0


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
        boxes, labels, scores = y5_model.predict(image_rgb)
        print("boxes: ", boxes)
        detections_queue.put([boxes, labels, scores, image_rgb])

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


def drawing(cam, detections_queue, frame_origin_queue, frame_final_queue, show_det=True):
    while cam.cap.isOpened():
        frame_origin, frame_count = frame_origin_queue.get()
        boxes, labels, scores, image_rgb = detections_queue.get()

        if frame_origin is not None:
            image = draw_det_when_track(frame_origin, boxes, scores=scores, labels=labels,
                                        class_names=class_names)
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
    frame_final_queue = Queue(maxsize=1)
    input_path = "/home/vuong/Desktop/Data/Clover/Video Register/Bùi Ngọc Thy Nhân.mp4"
    cam = InfoCam(input_path)

    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue, frame_origin_queue))
    thread2 = KThread(target=inference, args=(cam, frame_detect_queue, detections_queue))
    thread4 = KThread(target=drawing, args=(cam, detections_queue, frame_origin_queue, frame_final_queue))

    thread_manager = []
    thread1.daemon = True  # sẽ chặn chương trình chính thoát khi thread còn sống.
    thread1.start()
    thread_manager.append(thread1)
    thread2.daemon = True
    thread2.start()
    thread_manager.append(thread2)
    thread4.daemon = True
    thread4.start()
    thread_manager.append(thread4)

    while cam.cap.isOpened():
        # cv2.namedWindow('output')
        image, frame_count = frame_final_queue.get()
        # image = cv2.resize(image, (1400, 640))
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

