import cv2
import numpy as np
import os
import time
from glob import glob

from app.mongo_dal.identity_dal import IdentityDAL
from core.main.face_detect.pytorch_retinaface.DSFDPytorchInference import face_detection
from core.main.main_utils.draw import draw_box_and_landmark
from core.main.main_utils.helper import convert_np_array_to_base64, read_url_img_to_array, align_face
from app.milvus_dal.clover_dal import MilvusCloverDAL

detector = face_detection.build_detector(
    "RetinaNetResNet50",  # RetinaNetResNet50, RetinaNetMobileNetV1
    # max_resolution=200
)


def test_detect_batch():
    impaths = "/home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/image_head"
    impaths = glob(os.path.join(impaths, "*.png"))
    impaths = impaths[:1]
    impaths = ["/home/vuong/Desktop/Project/GG_Project/clover/Test/image/test_2.png"]
    image = None
    for i, impath in enumerate(impaths):
        if impath.endswith("out.jpg"):
            continue
        im = cv2.imread(impath)
        im = cv2.resize(im, (1000, 1000), interpolation=cv2.INTER_AREA)
        im = im[:, :, ::-1]
        if i == 0:
            batch_im = im[None, :, :, :]
        else:
            # batch_im = np.concatenate((batch_im, im), axis=0)
            batch_im = np.vstack((batch_im, im[None, :, :, :]))
    t = time.time()
    dets = detector.batched_detect_with_landmarks(batch_im)
    bbox = dets[0][0]
    landmark = dets[1][0]

    image = cv2.imread(impaths[0])
    image = cv2.resize(image, (1000, 1000), interpolation=cv2.INTER_AREA)
    image = draw_box_and_landmark(image, bbox, landmark)
    xmin, ymin, xmax, ymax = list(map(int, bbox[0][:4]))
    cv2.imwrite("/home/vuong/Desktop/Project/GG_Project/clover/Test/image/face.png", image[ymin:ymax, xmin:xmax])
    # cv2.imshow("test", image)
    # cv2.waitKey(0)
    image = align_face(image, bbox[0], landmark[0])
    cv2.imwrite("/home/vuong/Desktop/Project/GG_Project/clover/Test/image/face_align.png", image)
    # cv2.imshow("test", image)
    # cv2.waitKey(0)

    print(f"Detection time: {time.time() - t:.3f}")


if __name__ == '__main__':

    test_detect_batch()