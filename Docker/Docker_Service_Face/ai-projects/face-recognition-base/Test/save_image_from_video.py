import cv2
import os
import shutil

url = "/storages/data/DATA/Clover_data/Identity/Nguyễn Tố Minh Phúc.mp4"  # lop clover

# path_save = "/media/vuong/AI1/Data_clover/Video_test/identity/Bùi_Thiện_Nhân/"
path_save = "/storages/data/DATA/Clover_data/Identity/Nguyễn_Tố_Minh_Phúc/"
if os.path.exists(path_save):
    shutil.rmtree(path_save)
os.makedirs(path_save)
# open the feed
cap = cv2.VideoCapture(url)
ret, frame = cap.read()
h, w, c = frame.shape
print(h, w, c)

count = 0
while True:
    # read next frame
    ret, frame = cap.read()
    if ret is False:
        break
    print(ret)
    # show frame to user
    cv2.imshow('frame', cv2.resize(frame, (1000, 500)))
    if count % 2 == 0:
        cv2.imwrite(path_save + "frame_" + str(count) + ".png", frame)

    # if user presses q quit program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    count += 1

# close the connection and close all windows
cap.release()
cv2.destroyAllWindows()