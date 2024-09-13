import cv2      # import the OpenCV library
import numpy as np  # import the numpy library

# input_path = "/storages/data/DATA/Video_Test/Test_sleepless.mp4"
input_path = '/home/vuong/Videos/Test_sleepless_q7_5561.mp4'

font = cv2.FONT_HERSHEY_SIMPLEX
video_capture = cv2.VideoCapture(input_path)

# importing the module
import cv2


# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)


# driver function
if __name__ == "__main__":
    # reading the image
    # img = cv2.imread('lena.jpg', 1)
    _, img = video_capture.read()
    img = cv2.resize(img, (700, 500))

    # displaying the image
    cv2.imshow('image', img)
    cv2.imwrite("/storages/data/DATA/Video_Test/Test_sleepless.png", img)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # close the window
    cv2.destroyAllWindows()