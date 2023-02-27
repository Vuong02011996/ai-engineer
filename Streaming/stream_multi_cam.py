import cv2
from queue import Queue
import os
from kthread import KThread
import numpy as np
import subprocess


def video_capture(frame_detect_queue, input_path):
    frame_count = 0
    cap = cv2.VideoCapture(input_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    while cap.isOpened():
        ret, frame_ori = cap.read()
        if not ret:
            while True:
                print("cam.cap.isOpened()", cap.isOpened())
                cap = cv2.VideoCapture(input_path)
                print("cam.cap.isOpened()", cap.isOpened())
                ret, frame_ori = cap.read()
                print("Camera can't read frame")
                if ret:
                    break

        # if frame_step != 0 and frame_count % frame_step != 0:
        #     continue
        frame_rgb = cv2.cvtColor(frame_ori, cv2.COLOR_BGR2RGB)
        frame_detect_queue.put([frame_rgb, frame_count])
        # print("frame_count: ", frame_count)
        frame_count += 1
        # frame_step += 2

    cap.release()


list_url_cam = [{"url": "rtsp://admin:HikC@mera@58.186.75.67:5555",
                 "name": "q7_cong_chinh_5555"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5561",
                 "name": "q7_mon2_5561"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5560",
                 "name": "q7_mon2_5560"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5557",
                 "name": "q7_pre2_5557"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5558",
                 "name": "q7_pre2_5558"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5562",
                 "name": "q7_nur_5562"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5563",
                 "name": "q7_nur_5563"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5564",
                 "name": "q7_pre1_5564"},
                {"url": "rtsp://admin:HikC@mera@58.186.75.67:5565",
                 "name": "q7_pre1_5565"},
                {"url": "rtsp://admin:HikC@mera@14.161.9.93:5559",
                 "name": "q2_cong_chinh_5559"},
                {"url": "rtsp://admin:HikC@mera@14.161.9.93:5568",
                 "name": "q2_tang_2_5568"},
                {"url": "rtsp://admin:HikC@mera@14.161.9.93:5569",
                 "name": "q2_tang_3_5569"},
                {"url": "rtsp://admin:HikC@mera@14.161.9.93:5570",
                 "name": "q2_tang_4_5570"},
                {"url": "rtsp://admin:HikC@mera@14.161.9.93:5571",
                 "name": "q2_tang_1_moi_5571"}]
show = True

if __name__ == '__main__':
    list_frame_detect_queue = []
    for i in range(len(list_url_cam)):
        list_frame_detect_queue.append(Queue(maxsize=1))

    thread_manager = []
    for i in range(len(list_url_cam)):
        thread = KThread(target=video_capture, args=(list_frame_detect_queue[i], list_url_cam[i]["url"]))
        thread_manager.append(thread)

    for i in range(len(list_url_cam)):
        thread_manager[i].daemon = True  # sẽ chặn chương trình chính thoát khi thread còn sống.
        thread_manager[i].start()

    num_col = 4
    if show is False:
        cap = cv2.VideoCapture(list_url_cam[0]["url"])
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        url_stream_server = "rtmp://0.0.0.0:55555/stream/stream_multi_cam"
        # command and params for ffmpeg
        command = ['ffmpeg',
                   '-y',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-s', "{}x{}".format(width, height),
                   '-r', str(20),
                   '-i', '-',
                   '-c:v', 'libx264',
                   '-pix_fmt', 'yuv420p',
                   '-preset', 'ultrafast',
                   '-f', 'flv',
                   url_stream_server]
        # ffmpeg -re -i INPUT_FILE_NAME -c copy -f flv rtmp://localhost/live/STREAM_NAME
        # using subprocess and pipe to fetch frame data
        # p = subprocess.Popen(command, stdin=subprocess.PIPE)
        process_stream = subprocess.Popen(command, stdin=subprocess.PIPE, preexec_fn=os.setsid)

    while True:
        combine_row_img = None
        combine_all_img = None
        for i in range(len(list_url_cam)):
            image, frame_count = list_frame_detect_queue[i].get()
            print("i: ", i)
            print("image.shape(): ", image.shape)
            img_array = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            img_array = cv2.resize(img_array, (300, 200), interpolation=cv2.INTER_AREA)
            img_array = cv2.putText(img_array, list_url_cam[i]["name"],
                                    (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 255, 0), 2)

            if combine_row_img is None:
                combine_row_img = img_array
            else:
                combine_row_img = np.hstack((combine_row_img, img_array))

            if (i + 1) % num_col == 0:
                # cv2.imwrite("image_test/" + name + ".png", combine_row_img)
                if combine_all_img is None:
                    combine_all_img = combine_row_img
                else:
                    combine_all_img = np.vstack((combine_all_img, combine_row_img))
                combine_row_img = None
            # if last row not enough num_col image
        if combine_row_img is not None:
            for i in range(int(num_col - (combine_row_img.shape[1] / 300))):
                combine_row_img = np.hstack((combine_row_img, np.zeros((200, 300, 3), dtype=np.uint8)))
            if combine_all_img is not None:
                combine_all_img = np.vstack((combine_all_img, combine_row_img))
            else:
                combine_all_img = combine_row_img
        if show:
            cv2.imshow("window", combine_all_img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
        else:
            img_array_show = cv2.resize(combine_all_img, (width, height), interpolation=cv2.INTER_AREA)
            process_stream.stdin.write(img_array_show.tobytes())