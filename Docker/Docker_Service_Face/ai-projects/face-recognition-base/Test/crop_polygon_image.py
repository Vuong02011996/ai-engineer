# https://www.life2coding.com/cropping-polygon-or-non-rectangular-region-from-image-using-opencv-python/

import numpy as np
import cv2


if __name__ == '__main__':

    img = cv2.imread("/storages/data/DATA/Video_Test/Test_sleepless.png")

    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    # points = np.array([[[100,350],[120,400],[310,350],[360,200],[350,20],[25,120]]])
    points = np.array([[196, 296], [544, 271], [572, 614], [186, 639]])

    #method 1 smooth region
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)

    #method 2 not so smooth region
    # cv2.fillPoly(mask, points, (255))

    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points) # returns (x,y,w,h) of the rect
    cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

    # ## crate the white background of the same size of original image
    # wbg = np.ones_like(img, np.uint8)*255
    # cv2.bitwise_not(wbg,wbg, mask=mask)
    # # overlap the resulted cropped image on the white background
    # dst = wbg+res

    # cv2.imshow('Original',img)
    # cv2.imshow("Mask",mask)
    cv2.imshow("Cropped", cropped )
    # cv2.imshow("Samed Size Black Image", res)
    # cv2.imshow("Samed Size White Image", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()