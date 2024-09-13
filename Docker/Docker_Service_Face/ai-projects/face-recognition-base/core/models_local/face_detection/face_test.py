import glob
import os
import cv2
import time
from core.models_local.face_detection.DSFDPytorchInference import face_detection
import numpy as np

detector = face_detection.build_detector(
    "RetinaNetMobileNetV1",  # DSFDDetector, RetinaNetResNet50, RetinaNetMobileNetV1
    max_resolution=200
)


def draw_faces(im, bboxes):
    for bbox in bboxes:
        x0, y0, x1, y1 = [int(_) for _ in bbox]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)


def detect_single():
    impaths = "/home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/image_head"
    impaths = glob.glob(os.path.join(impaths, "*.png"))
    # impaths = ["/home/vuong/Desktop/Project/MyGitHub/MOT_tracking/mot_sort/Case_error/case_maching_error_1_solved/test_1679.png"]
    total_time = 0
    for impath in impaths:
        if impath.endswith("out.jpg"):
            continue
        im = cv2.imread(impath)
        print("Processing:", impath)
        t = time.time()
        dets = detector.detect(
            im[:, :, ::-1]
        )[:, :4]
        total_time += time.time() - t
        print(f"Detection time: {time.time() - t:.3f}")
        draw_faces(im, dets)
        imname = os.path.basename(impath).split(".")[0]
        output_path = os.path.join(
            os.path.dirname(impath),
            f"{imname}_out.jpg"
        )

        cv2.imwrite(output_path, im)
    print("total_time: ", total_time)


def test_detect_batch():
    impaths = "/home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/image_head"
    impaths = glob.glob(os.path.join(impaths, "*.png"))
    impaths = impaths[:10]
    # impaths = [impaths[0]]
    for i, impath in enumerate(impaths):
        if impath.endswith("out.jpg"):
            continue
        im = cv2.imread(impath)
        im = cv2.resize(im, (200, 200), interpolation=cv2.INTER_AREA)
        im = im[:, :, ::-1]
        if i == 0:
            batch_im = im[None, :, :, :]
        else:
            # batch_im = np.concatenate((batch_im, im), axis=0)
            batch_im = np.vstack((batch_im, im[None, :, :, :]))
    t = time.time()
    dets = detector.batched_detect_with_landmarks(batch_im)
    print(f"Detection time: {time.time() - t:.3f}")


def detect_batch(batch_im):
    if batch_im is not None:
        dets = detector.batched_detect_with_landmarks(batch_im)
        return dets
    else:
        return []


def detect_face_bbox_head_batch(batch_im_head, x_offset, y_offset, w_scale, h_scale):
    boxes_face = np.zeros((batch_im_head.shape[0], 5))
    landmarks_face = np.zeros((batch_im_head.shape[0], 5, 2))

    result_detect = detector.batched_detect_with_landmarks(batch_im_head)
    boxes_det, landmarks = result_detect[0], result_detect[1]
    # one image head only one face
    for image_id in range(len(boxes_det)):
        if len(boxes_det[image_id]) > 0 and boxes_det[image_id][0][-1] > 0.9:
            box_face = boxes_det[image_id][0]
            landmark_detect = landmarks[image_id][0]  # index 0 because one face in image head

            box_face[0] *= w_scale[image_id]
            box_face[1] *= h_scale[image_id]
            box_face[2] *= w_scale[image_id]
            box_face[3] *= h_scale[image_id]

            box_face[0] += x_offset[image_id]
            box_face[1] += y_offset[image_id]
            box_face[2] += x_offset[image_id]
            box_face[3] += y_offset[image_id]

            for i, point in enumerate(landmark_detect):
                landmark_detect[i][0] *= w_scale[image_id]
                landmark_detect[i][1] *= h_scale[image_id]

                landmark_detect[i][0] += x_offset[image_id]
                landmark_detect[i][1] += y_offset[image_id]

            boxes_face[image_id] = box_face
            landmarks_face[image_id] = landmark_detect
        else:
            boxes_face[image_id] = np.zeros(5)
            landmarks_face[image_id] = np.zeros((5, 2))
    return boxes_face, landmarks_face


if __name__ == "__main__":
    detect_single()
    test_detect_batch()
