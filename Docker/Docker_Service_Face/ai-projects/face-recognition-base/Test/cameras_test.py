import cv2
import requests

# insert the HTTP(S)/RSTP feed from the camera
# url = "rtsp://admin:Admin123@14.241.120.239:554/1"
# url = "rtsp://admin:Admin123@14.241.120.239:554/video"
# url = "rtsp://admin:Admin123@14.241.120.239:554"  # ptz 360 cong ty
# url = "rtsp://admin:Admin123@14.241.120.239:556"  # bai xe cty
# url = "rtsp://admin:Admin123@14.241.120.239:555/video" # Hanh lang cty
# url = "rtsp://admin:HikC@mera@58.186.75.67:5557"  # cong truong clover
# url = "rtsp://admin:HikC@mera@14.161.9.93:5570"  # cong truong clover
# url = "/media/vuong/AI1/Data_clover/Video_test/identity/39fe6b44-cd6a-3cf1-1811-8a0851959e0d.mp4"  # lop clover
url = "rtsp://digesttest2:Oryza@123@192.168.111.63:7001/c4bd5a0e-95a4-1391-4170-504b25b81d63"


def show_cam():
    # open the feed
    cap = cv2.VideoCapture(url)

    while True:
        # read next frame
        ret, frame = cap.read()
        print(ret)

        # show frame to user
        cv2.imshow('frame', cv2.resize(frame, (1000, 500)))

        # if user presses q quit program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # close the connection and close all windows
    cap.release()
    cv2.destroyAllWindows()


def get_url_first_frame_cam():
    # open the feed
    url_cam = "rtsp://admin:HikC@mera@58.186.75.67:5561"
    # path_save_frame = "/home/vuong/Pictures/image_test"
    path_save_frame = "/storages/data/DATA/Clover_data/image_test"
    file_name = url_cam.split("@")[-1]
    cap = cv2.VideoCapture(url_cam)

    while True:
        # read next frame
        ret, frame = cap.read()
        print(ret)
        if ret:
            cv2.imwrite(path_save_frame + "/" + file_name + ".png", frame)
            # show frame to user
            url_api = 'https://erp-clover-file.demo.greenglobal.com.vn/api/files'
            url_server = 'https://erp-clover-file.demo.greenglobal.com.vn'
            data = {'files': open(path_save_frame + "/" + file_name + ".png", 'rb')}

            # array_img = cv2.imread('/home/gg-greenlab/Downloads/index.jpg')
            # data = {"files:": array_img}
            url = requests.post(url_api, files=data)
            url_output = url_server + url.json()["results"][0]["fileInfo"]["url"]
            print(url_output)
            cv2.imshow('frame', cv2.resize(frame, (1000, 500)))
            break

        # if user presses q quit program
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # close the connection and close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # get_url_first_frame_cam()
    show_cam()