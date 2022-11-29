import cv2
import requests

# insert the HTTP(S)/RSTP feed from the camera
# url = "rtsp://admin:Admin123@14.241.120.239:554/1"
# url = "rtsp://admin:Admin123@14.241.120.239:554/video"
# url = "rtsp://admin:Admin123@14.241.120.239:554"  # ptz 360 cong ty
# url = "rtsp://admin:Admin123@14.241.120.239:556"  # bai xe cty
# url = "rtsp://admin:Admin123@14.241.120.239:555/video" # Hanh lang cty
# url = "rtsp://admin:HikC@mera@58.186.75.67:5557"  # cong truong clover
url = "rtsp://admin:HikC@mera@58.186.75.67:5555"  # cong truong clover
# url = "/media/vuong/AI1/Data_clover/Video_test/identity/39fe6b44-cd6a-3cf1-1811-8a0851959e0d.mp4"  # lop clover


def show_cam():
    # open the feed
    cap = cv2.VideoCapture(url)
    print("CAP_PROP_FPS: ", cap.get(cv2.CAP_PROP_FPS))
    print("CAP_PROP_FRAME_WIDTH: ", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("CAP_PROP_BITRATE: ", cap.get(cv2.CAP_PROP_BITRATE))
    print("CAP_PROP_CODEC_PIXEL_FORMAT: ", cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT))
    print("CAP_PROP_FORMAT: ", cap.get(cv2.CAP_PROP_FORMAT))
    print("CV_CAP_PROP_FOURCC: ", cap.get(cv2.CAP_PROP_FOURCC))
    while True:
        # read next frame
        ret, frame = cap.read()
        print(ret)

        # show frame to user
        cv2.imshow('frame', cv2.resize(frame, (1000, 500)))
        cv2.imwrite("test.png", frame)
        break

        # # if user presses q quit program
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break

    # close the connection and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    show_cam()