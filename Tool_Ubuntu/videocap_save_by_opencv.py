import cv2
import threading
import queue
import signal
import sys
import time

stop = False

def signal_handler(signal, frame):
    
    global stop
    stop = True
    

def video_save_threading(video_filename, width, height, fps_video, quality_percen, frame_queue):

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video_write = cv2.VideoWriter(video_filename, fourcc, fps_video, (width, height))
    if quality_percen is not None:
        video_write.set(cv2.VIDEOWRITER_PROP_QUALITY, quality_percen)
        print("quality_percen : ", quality_percen)


    
    last_time = time.time()
    save_count = 0

    while True:
        if not frame_queue.empty():
            [index, frame] = frame_queue.get()
            if index != -1:
                video_write.write(frame)
                save_count += 1
                # print("save index = ", index)
            else:
                video_write.release()
                print("index != -1")
                break
        else:
            time.sleep(0.005)

        duration_time = time.time() - last_time
        if duration_time >= 5:
            last_time = time.time()
            print("video write fps : ", save_count/duration_time)            
            save_count = 0


def read_video(rtsp, video_filename, quality_percen=None):

    global stop
    frame_queue = queue.Queue(100)
    # wait_stop = threading.Barrier(2)

    if rtsp is None:
        rtsp = "rtsp://admin:Admin123@192.168.111.211/ch1/mainstream"
    else:
        print("rtsp : ", rtsp)


    video_capture = cv2.VideoCapture(rtsp)
    width = int(video_capture.get(3))
    height = int(video_capture.get(4))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    fps_video = fps if fps <= 120 else 30
    
    write_thread = threading.Thread(target=video_save_threading, args=[video_filename, width, height, fps_video, quality_percen, frame_queue])
    write_thread.start()

    small_frame = None
    index = 0
    last_time = time.time()
    read_count = 0
    while True:
        ret, frame_ori = video_capture.read()
        read_count += 1

        if ret:
            h,w = frame_ori.shape[0:2]
            if (not frame_queue.full()):
                frame_queue.put([index, frame_ori])
            else:
                print("drop frame at index : ", index)

            if (w > 1920):
                f = min(1920.0/w, 1080/h) 

                if small_frame is None:
                    small_frame = cv2.resize(frame_ori, (0, 0), fx=f, fy=f)
                else:
                    cv2.resize(frame_ori, (small_frame.shape[1], small_frame.shape[0]), dst=small_frame)
                
                cv2.imshow("abc", small_frame)
            else:
                cv2.imshow("abc", frame_ori)

            
            key = cv2.waitKey(5)
            index += 1
            # print("read index = ", index)

            if (key & 0xFF00 == 0):  # normal keys press
                if (key & 0xFF) in [ord('q'), ord('Q'), 27]:
                    stop = True

        else:
            print("stop-cam")
            frame_queue.put([-1, frame_ori])
            break

        if stop:
            frame_queue.put([-1, None])
            break
        
        duration_time = time.time() - last_time
        if duration_time >= 5:
            last_time = time.time()
            print("came read fps : ", read_count/duration_time)
            read_count = 0

    video_capture.release()

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print(
        "------------------------------------------------------------------------------------\n"
        "Call this program like this:\n\n"
        "python  ./videocap_save_by_opencv.py <rtsp_cam> <save_video_file_name> [quality_percen]"
        "\n"
        )
    
        exit()

    
    print("Q or Esc keypress: Quit")
    print('\n\n-----------------------------------------------------------------------------------\n')

    signal.signal(signal.SIGINT, signal_handler)

    rtsp = sys.argv[1]
    video_filename = sys.argv[2]
    quality_percen = None

    if len(sys.argv) >= 3:
        quality_percen = int(sys.argv[3])


    read_video(rtsp, video_filename, quality_percen)

    # python videocap_save_by_opencv.py "rtsp://admin:Admin123@192.168.111.211/ch1/mainstream" abc1.mp4 99

