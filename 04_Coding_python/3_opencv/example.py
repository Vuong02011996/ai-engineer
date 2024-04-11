import cv2


def show_test():
    image_show = None
    cv2.imshow('test', image_show)
    if cv2.waitKey() & 0xFF == ord("q"):
        cv2.destroyWindow('test')