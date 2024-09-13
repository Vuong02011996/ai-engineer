import cv2
from queue import Queue
import time
from kthread import KThread
import numpy as np
from datetime import datetime
# from app.services.attendance.attendance_helper import get_coordinates_roll_call_from_process_name
from core.main.video_capture import video_capture
# from core.main.head_detect import head_detect, head_detect_service
from core.main.head_detect import head_detect, head_detect_service

from core.main.tracking import tracking
from core.main.detect_face_v2 import detect_face_bbox_head_v1
from core.main.recognize_face import get_face_features
from core.main.matching_identity import matching_identity
from core.main.export_data_vms import export_data
from core.main.drawing import drawing, drawing_v2
from app.mongo_dal.object_dal.object_attendance_dal import ObjectAttendanceDAL
from app.mongo_dal.process_dal.process_attendance_dal import ProcessAttendanceDAL

object_dal = ObjectAttendanceDAL()
process_dal = ProcessAttendanceDAL()


class InfoCam(object):
    def __init__(self, cam_name, process_name, address, test_video):
        print("cam_name: ", cam_name)
        self.cap = cv2.VideoCapture(cam_name)
        self.resize = False
        if self.resize:
            self.width = int(640)
            self.height = int(640)
        else:
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.total_frame_video = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_start = 0

        self.process_name = process_name
        self.address = address
        # coordinates = get_coordinates_roll_call_from_process_name(process_name, self.width, self.height)
        # if coordinates is not None:
        #     # coordinates trả về theo tọa độ :
        #     # top, left 0 -> bottom, left 1  -> bottom, right 2 -> top, right 3
        #     # region track lại mong muốn thứ tự top, left 0-> top, right 3-> bottom, right 2-> bottom, left 1
        #     # Đúng ra phải là self.region_track = [coordinates[0], coordinates[3], coordinates[2], coordinates[1]]
        #     # Nhưng mà ...
        #     self.region_track = [coordinates[0], coordinates[2], coordinates[3], coordinates[1]]
        #     # self.region_track = coordinates
        # else:
        coordinates = np.array([[0, 0], [self.width-50, 0], [self.width-50, self.height-50], [0, self.height-50]])
        self.region_track = [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]

        ## test region
        # self.region track yêu cầu: Hồng(tl-0) -> trắng(tr-1) ->  xanh lam(br-3) -> đỏ(bl-2),
        # ret, frame_ori = self.cap.read()
        # # frame_ori = cv2.rectangle(frame_ori, tuple(coordinates[0]), tuple(coordinates[2]), (0, 0, 255), 2)
        # frame_ori = cv2.circle(frame_ori, tuple(self.region_track[0]), radius=5, color=(255, 0, 255), thickness=10) # Hồng
        # frame_ori = cv2.circle(frame_ori, tuple(self.region_track[1]), radius=5, color=(255, 255, 255), thickness=10) # trắng
        # frame_ori = cv2.circle(frame_ori, tuple(self.region_track[3]), radius=5, color=(0, 0, 255), thickness=10) # xanh lam
        # frame_ori = cv2.circle(frame_ori, tuple(self.region_track[2]), radius=5, color=(255, 0, 0), thickness=10) # đỏ
        # frame_ori = draw_region(frame_ori, self.region_track)
        # cv2.imshow('output_roll_call', cv2.resize(frame_ori, (800, 500)))
        # cv2.waitKey(0)

        self.frame_step_after_track = 0
        self.show_all = False
        self.test_video = test_video


def run_roll_call(item_cam, process_name, end_time_s, info_cam_running, address, test_video=False, cv2_show=True, window="test"):
    print("vào run_roll_call...")
    start_time = time.time()
    frame_detect_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    show_all_queue = Queue(maxsize=1)
    frame_final_queue = Queue(maxsize=1)
    face_embedding_queue = Queue(maxsize=1)
    head_bbox_queue = Queue(maxsize=1)
    matching_queue = Queue(maxsize=1)
    show_queue = Queue(maxsize=1)
    database_queue = Queue(maxsize=1)

    if test_video:
        input_path = item_cam
    else:
        input_path = item_cam["url_cam"]
    cam = InfoCam(input_path, process_name, address, test_video)
    # -------------------------------------------------------------------------
    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue, input_path))
    thread2 = KThread(target=head_detect_service, args=(cam, frame_detect_queue, detections_queue, info_cam_running))
    # thread2 = KThread(target=head_detect, args=(cam, frame_detect_queue, detections_queue))
    thread3 = KThread(target=tracking, args=(cam, detections_queue, show_all_queue, head_bbox_queue))
    thread4 = KThread(target=detect_face_bbox_head_v1, args=(cam, head_bbox_queue, face_embedding_queue, info_cam_running, object_dal))
    thread5 = KThread(target=get_face_features, args=(cam, face_embedding_queue, matching_queue, info_cam_running))
    thread6 = KThread(target=matching_identity, args=(cam, matching_queue, database_queue, show_queue))
    thread7 = KThread(target=export_data, args=(cam, database_queue, object_dal, info_cam_running))
    if cv2_show:
        thread8 = KThread(target=drawing_v2, args=(cam, show_queue, show_all_queue, frame_final_queue, object_dal))

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
    thread7.daemon = True
    thread7.start()
    thread_manager.append(thread7)
    thread8.daemon = True
    thread8.start()
    thread_manager.append(thread8)

    while cam.cap.isOpened():
        image, frame_count = frame_final_queue.get()
        # if test_video is False:
        #     print("frame_count_" + item_cam["id_camera"] + ":    ", frame_count)

        # STREAMING
        # if process_stream is not None:
        #     process_stream.stdin.write(image.tobytes())

        # if cv2_show:
        #     # image_show = cv2.resize(image, (1200, 706))
        #     image_show = cv2.resize(image, (700, 500))
        #     cv2.imshow(window, image_show)
        #     if cv2.waitKey(1) & 0xFF == ord("q"):
        #         cv2.destroyWindow(window)
        #         break

        # # Get time current
        # time_utc_now = datetime.utcnow()
        # time_now_seconds = time_utc_now.timestamp()
        # if time_now_seconds >= end_time_s:
        #     print("time_current: ", time_now_seconds)
        #     print("end_time_roll_call_s: ", end_time_s)
        #     break

    total_time = time.time() - start_time
    print("FPS video: ", cam.fps)
    print("Total time: {}, Total frame: {}, FPS all process : {}".format(total_time, cam.total_frame_video,
                                                                         1 / (total_time / cam.total_frame_video)), )

    for t in thread_manager:
        if t.is_alive():
            t.terminate()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # input_path = "rtsp://admin:Admin123@14.241.120.239:554"
    # input_path = "/home/vuong/Videos/test_phu.mp4"
    input_path = "/home/oryza/Videos/Video_test_acc2.mp4"
    # input_path = "/root/vuong/face_test/Video_test_acc2.mp4"  # server 1

    # Cam chinh co ai diem danh
    # input_path = "rtsp://oryza2:Oryza@2024@192.168.111.77:554/0/profile4/media.smp"

    # Cam goc truoc mat
    # input_path = "rtsp://digesttest:a0sm9u0pZgJufg5@192.168.111.59:7001/9a5dcef8-8028-5c36-56b9-ee51381f454d"

    # Cam phong kinh doanh
    # input_path = "rtsp://digesttest:a0sm9u0pZgJufg5@192.168.111.59:7001/386d79aa-5797-f5f6-b88e-219f81e09e04"

    process_stream = None
    process_name = "660bd63917d3c6720b8817ab_roll_call_18_2024:04:02-17:27:07"
    # process_name = "6618ed5b28839f58a2d0ecf4_roll_call_6_2024:04:12-15:20:01"  # server 1
    thread_safe_region_manager = []
    time_now = datetime.now()
    time_now_seconds = time_now.timestamp()
    end_time_s = time_now_seconds + 5000
    port_model_head = '5000'
    port_model_insight = '18081'
    info_cam_running = {
        "ip_host_socket": "192.168.111.63",
        "port_host_socket": 2203,
        "port_model_head": '5000',
        "port_model_insight": '18081'
    }
    address = ''
    run_roll_call(input_path, process_name, end_time_s, info_cam_running, address, test_video=True, cv2_show=True)
