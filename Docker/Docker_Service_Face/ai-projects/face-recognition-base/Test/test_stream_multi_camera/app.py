from flask import Flask, render_template, Response, request
import cv2
import threading
from queue import Queue
from kthread import KThread

app = Flask(__name__)


outputFrame = None
input_path = None
lock = threading.Lock()


class InfoCam(object):
    def __init__(self, cam_name):
        self.cap = cv2.VideoCapture(cam_name)
        self.frame_start = 0
        self.total_frame_video = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps_video = int(self.cap.get(cv2.CAP_PROP_FPS))


def video_capture(cam, frame_detect_queue):
    frame_count = cam.frame_start
    # frame_step = 2
    # frame_using = 0
    cam.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    while cam.cap.isOpened():
        ret, frame_ori = cam.cap.read()
        # if frame_using != 0 and frame_count % frame_using != 0:
        #     frame_count += 1
        #     continue
        if not ret:
            break

        # frame_ori = adjust_gamma(frame_ori, gamma=0.35)
        frame_detect_queue.put([frame_ori, frame_count])
        print("frame_count: ", frame_count)
        frame_count += 1
        # frame_using += frame_step

    cam.cap.release()


def find_camera(id):
    cameras = ['https://minio.core.greenlabs.ai/clover/motion_detection/activity_5554_31_3_2021.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20211007%2F%2Fs3%2Faws4_request&X-Amz-Date=20211007T064528Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=1a2c56bdf9dbd6784b492847ec553596b80a8038de5cfbc763d5563c84de5282',
               'https://minio.core.greenlabs.ai/clover/motion_detection/camera554-4-fullhd-nghitrua.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20211007%2F%2Fs3%2Faws4_request&X-Amz-Date=20211007T064105Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=127364303df9c38b5453d8c0949bff3c03ddd1d937d2a227c14d3adacaab15b1']
    return cameras[int(id)]

#  for webcam use zero(0)


def get_frame_to_show():
    global outputFrame, lock, input_path

    frame_detect_queue = Queue(maxsize=1)
    cam = InfoCam(input_path)
    thread1 = KThread(target=video_capture, args=(cam, frame_detect_queue))
    thread_manager = []
    thread1.daemon = True  # sẽ chặn chương trình chính thoát khi thread còn sống.
    thread1.start()
    thread_manager.append(thread1)
    while cam.cap.isOpened():
        frame_ori, frame_count = frame_detect_queue.get()

        # lock
        with lock:
            outputFrame = frame_ori.copy()

    for t in thread_manager:
        if t.is_alive():
            t.terminate()
    cv2.destroyAllWindows()


def gen_frames(camera_id):

    cam = find_camera(camera_id)
    cap = cv2.VideoCapture(cam)

    while True:
        # for cap in caps:
        # # Capture frame-by-frame
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def generate(camera_id):
    cam = find_camera(camera_id)
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/start_video_motion", methods=['POST'])
def start_video():
    global input_path
    #  https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
    if request.method == 'POST':
        file = request.form["name"]
        input_path = file
        t = KThread(target=get_frame_to_show)
        t.daemon = True
        t.start()
    # return the rendered template
    return "<p>OK!</p>"


@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=["GET"])
def index():
    return render_template('index_add_camera.html', my_list=[0, 1])


if __name__ == '__main__':
    app.run()