import traceback
from datetime import datetime

import cv2
import time
from sentry_sdk import capture_message

from app.app_utils.file_io_untils import ip_run_service_ai


def video_capture(cam, frame_detect_queue, input_path, save_video=False):
    frame_count = cam.frame_start
    frame_step = 2
    frame_using = 0
    cam.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    if save_video:
        # https://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/
        # https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html#gsc.tab=0
        # https://stackoverflow.com/questions/30103077/what-is-the-codec-for-mp4-videos-in-python-opencv
        # VideoWriter (const String &filename, int fourcc, double fps, Size frameSize, bool isColor=true)
        size = (cam.width, cam.height)
        writer = cv2.VideoWriter(cam.path_image + cam.process_name + ".mp4",
                                 cv2.VideoWriter_fourcc(*'MP4V'),  # X264, MJPG, MPEG
                                 cam.fps, size)
    else:
        writer = None

    while cam.cap.isOpened():
        start_time = time.time()
        ret, frame_ori = cam.cap.read()
        if frame_using != 0 and frame_count % frame_using != 0:
            frame_count += 1
            continue
        if cam.test_video is True and not ret:
            break
        if not ret and cam.test_video is False:
            while True:
                print("cam.cap.isOpened()", cam.cap.isOpened())
                cam.cap.release()
                cam.cap = cv2.VideoCapture(input_path)
                print("cam.cap.isOpened()", cam.cap.isOpened())
                ret, frame_ori = cam.cap.read()
                print("Camera can't read frame")
                capture_message(
                    f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] Camera can't read frame:  " + str(cam.url_cam))
                if ret:
                    break
        frame_rgb = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2RGB)

        if cam.resize:
            frame_rgb = cv2.resize(frame_rgb, (cam.width, cam.height))

        # print("##################################")
        # print("video_capture cost", time.time() - start_time)
        frame_detect_queue.put([frame_rgb, frame_count])
        # print("frame_count: ", frame_count)
        frame_count += 1
        frame_using += frame_step

        # Write the frame into the
        # file 'filename.avi'
        if writer is not None:
            writer.write(frame_ori)

    cam.cap.release()
    if writer is not None:
        writer.release()


if __name__ == '__main__':
    pass