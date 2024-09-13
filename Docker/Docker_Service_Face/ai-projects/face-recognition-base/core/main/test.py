import os
import subprocess
import cv2
from queue import Queue
import time
from kthread import KThread
import threading
import numpy as np
from core.main.video_capture import video_capture
from core.main.head_detect import head_detect
from core.main.tracking import tracking
from core.main.detect_face import detect_face_bbox_head
from core.main.recognize_face import get_face_features
from core.main.matching_identity import matching_identity
from core.main.export_data_v2 import export_data
from core.main.drawing import drawing

from flask import Response
from flask import render_template
from flask import Blueprint, request

# outputFrame = None
# lock = threading.Lock()

# blueprint = Blueprint("Roll_Call_App", __name__)

# input_path = None


class InfoCam(object):
    def __init__(self, cam_name):
        self.cap = cv2.VideoCapture(cam_name)
        self.frame_start = 0
        self.total_frame_video = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps_video = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.process_name = cam_name.split("/")[-1].split(".")[0]
        self.region_track = np.array([[0, 0],
                                      [2560, 0],
                                      [2560, 1440],
                                      [0, 1440]])
        self.frame_step_after_track = 0
        self.show_all = False

        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def run_roll_call(input_path, url_stream_server):
    start_time = time.time()
    # global outputFrame, lock  # input_path
    cv2_show = False
    if cv2_show:
        #  "/storages/data/clover_project/Videos-bk/diemdanh/diem_danh_deo_khau_trang2.mp4"
        input_path = "/home/vuong/Desktop/Data/Clover/Video diem danh/diem_danh_deo_khau_trang2.mp4"
    frame_detect_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    show_all_queue = Queue(maxsize=1)
    frame_final_queue = Queue(maxsize=1)
    face_embedding_queue = Queue(maxsize=1)
    head_bbox_queue = Queue(maxsize=1)
    matching_queue = Queue(maxsize=1)
    show_queue = Queue(maxsize=1)
    database_queue = Queue(maxsize=1)
    # input_path = "/home/vuong/crop4.mp4"
    cam = InfoCam(input_path)
    # For Streaming -----------------------------------------------------------
    # command and params for ffmpeg
    command = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', "{}x{}".format(cam.width, cam.height),
               '-r', str(cam.fps),
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               url_stream_server]
    # ffmpeg -re -i INPUT_FILE_NAME -c copy -f flv rtmp://localhost/live/STREAM_NAME
    # using subprocess and pipe to fetch frame data
    p = subprocess.Popen(command, stdin=subprocess.PIPE)

    # -------------------------------------------------------------------------

    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue))
    thread2 = KThread(target=head_detect, args=(cam, frame_detect_queue, detections_queue))
    thread3 = KThread(target=tracking, args=(cam, detections_queue, show_all_queue, head_bbox_queue))
    thread4 = KThread(target=detect_face_bbox_head, args=(cam, head_bbox_queue, face_embedding_queue))
    thread5 = KThread(target=get_face_features, args=(cam, face_embedding_queue, matching_queue))
    thread6 = KThread(target=matching_identity, args=(cam, matching_queue, database_queue, show_queue))
    thread7 = KThread(target=export_data, args=(cam, database_queue))
    thread8 = KThread(target=drawing, args=(cam, show_queue, show_all_queue, frame_final_queue))

    thread_roll_call_manager = []
    thread1.daemon = True  # sẽ chặn chương trình chính thoát khi thread còn sống.
    thread1.start()
    thread_roll_call_manager.append(thread1)
    thread2.daemon = True
    thread2.start()
    thread_roll_call_manager.append(thread2)
    thread3.daemon = True
    thread3.start()
    thread_roll_call_manager.append(thread3)
    thread4.daemon = True
    thread4.start()
    thread_roll_call_manager.append(thread4)
    thread5.daemon = True
    thread5.start()
    thread_roll_call_manager.append(thread5)
    thread6.daemon = True
    thread6.start()
    thread_roll_call_manager.append(thread6)
    thread7.daemon = True
    thread7.start()
    thread_roll_call_manager.append(thread7)
    thread8.daemon = True
    thread8.start()
    thread_roll_call_manager.append(thread8)

    while cam.cap.isOpened():
        image, frame_count = frame_final_queue.get()
        print("frame_count: ", frame_count)
        # image = cv2.resize(image, (1400, 640))
        # acquire the lock, set the output frame, and release the
        # lock
        # with lock:
        #     outputFrame = image.copy()

        # STREAMING
        # write to pipe
        p.stdin.write(image.tobytes())

        if cv2_show:
            cv2.imshow('output', image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyWindow('output')
                break

    total_time = time.time() - start_time
    print("FPS video: ", cam.fps_video)
    print("Total time: {}, Total frame: {}, FPS all process : {}".format(total_time, cam.total_frame_video,
                                                                         1 / (total_time / cam.total_frame_video)), )

    for t in thread_roll_call_manager:
        if t.is_alive():
            t.terminate()
    cv2.destroyAllWindows()


# def generate():
#     # grab global references to the output frame and lock variables
#     global outputFrame, lock
#     # loop over frames from the output stream
#     while True:
#         # wait until the lock is acquired
#         with lock:
#             # check if the output frame is available, otherwise skip
#             # the iteration of the loop
#             if outputFrame is None:
#                 continue
#             # encode the frame in JPEG format
#             (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
#             # ensure the frame was successfully encoded
#             if not flag:
#                 continue
#         # yield the output frame in the byte format
#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                bytearray(encodedImage) + b'\r\n')
#
#
# @blueprint.route('/stream_roll_call')
# def stream():
#     # return the rendered template
#     return render_template(os.getenv("HTML_STREAM"))
#
#
# @blueprint.route('/start_video_roll_call', methods=['POST'])
# def start_video():
#     # global input_path
#     #  https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
#     if request.method == 'POST':
#         file = request.form["name"]
#         input_path = file
#         t = KThread(target=run_roll_call, args=(input_path,))
#         t.daemon = True
#         t.start()
#     # return the rendered template
#     options = {"status": True, "status_code": 200, "message": "Start function roll call successfully!",
#                "stream_url": "http://14.241.120.239:8001/clover/test/v2.0/stream_roll_call"}
#     return options
#
#
# @blueprint.route('/stop_video_roll_call', methods=['POST'])
# def stop_video():
#     # global input_path
#     #  https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
#     if request.method == 'POST':
#         file = request.form["name"]
#         input_path = file
#         t = KThread(target=run_roll_call, args=(input_path,))
#         t.daemon = True
#         t.start()
#     # return the rendered template
#     options = {"status": True, "status_code": 200, "message": "Stop video {file} roll call successfully!"}
#     return options
#
#
# @blueprint.route('/video_feed_roll_call')
# def video_feed():
#     # return the response generated along with the specific media
#     # type (mime type)
#     return Response(generate(),
#                     mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    input_path = "https://minio.core.greenlabs.ai/local/demo_video/test_diem_danh.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20220105%2F%2Fs3%2Faws4_request&X-Amz-Date=20220105T083300Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=22dae69f13a06dd617397f5dfc972ef0dc79a2cb7bc58f33cc9d3a4d9d08f5e9"
    url_stream_server = "rtmp://0.0.0.0:55555/stream/test"
    run_roll_call(input_path, url_stream_server)
    # # # start the flask app
    # app.run(host="0.0.0.0", port="33333", debug=True,
    #         threaded=True, use_reloader=False)
