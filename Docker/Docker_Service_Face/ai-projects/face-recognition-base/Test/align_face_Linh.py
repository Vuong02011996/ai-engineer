import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)
import numpy as np
import cv2
from skimage import transform as trans
from collections.abc import Iterable

"https://pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/"


class BaseFaceAligner(object):
    def __init__(self) -> None:
        pass


def read_image(image, resize=None, gray=False):
    if isinstance(image, str):
        with open(image, "rb") as img_f:
            chunk = img_f.read()
            chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
            img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
    else:
        img = image

    if resize is not None:
        if isinstance(resize, Iterable) and len(resize) == 2:
            img = cv2.resize(img, resize)

    if gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


class FaceAligner():
    __instance = None

    def __init__(self, exp_width=112, exp_height=112, eye_height=[0.3, 0.3], n_landmarks=5):
        if FaceAligner.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.exp_width = exp_width
            self.exp_height = exp_height
            self.eye_height = eye_height
            self.eye_distance = 1. - self.eye_height[0] * 2
            self.n_landmarks = n_landmarks
            FaceAligner.__instance = self

    @staticmethod
    def getInstance(exp_width=112, exp_height=112, eye_height=[0.3, 0.3], n_landmarks=5):
        if FaceAligner.__instance == None:
            FaceAligner(exp_width, exp_height, eye_height, n_landmarks)
        return FaceAligner.__instance

    def align_with_M(self, image, bbox, points):
        if isinstance(image, str):
            image = read_image(image)

        bbx, bby, bbw, bbh = bbox

        if isinstance(points, dict):
            leye_x, leye_y = points["left_eye"]
            reye_x, reye_y = points["right_eye"]
        else:
            leye_x, leye_y = points[0]
            reye_x, reye_y = points[1]

        leye_x = leye_x - bbx
        leye_y = leye_y - bby
        reye_x = reye_x - bbx
        reye_y = reye_y - bby

        face = image[int(bby):int(bby + bbh), int(bbx):int(bbx + bbw), :]

        dx = reye_x - leye_x
        dy = reye_y - leye_y
        angle = np.degrees(np.arctan2(dy, dx))

        distance = np.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            scale = 1
        else:
            scale = (self.exp_width * self.eye_distance) / distance

        face_center = [int((leye_x + reye_x) // 2), int((leye_y + reye_y) // 2)]

        M = cv2.getRotationMatrix2D(face_center, angle, scale)

        tX = self.exp_width * 0.5
        tY = self.exp_height * self.eye_height[0]
        M[0, 2] += (tX - face_center[0])
        M[1, 2] += (tY - face_center[1])

        face = cv2.warpAffine(face, M, (self.exp_width, self.exp_height))

        return face, M

    # def align(self, image, bbox, points, timer=False):
    #     # # print(bbox, points)
    #     if timer:
    #         start=time.time()
    #         if self.n_landmarks==5:
    #             face=self._align_(image, bbox, points)
    #         stop=time.time()
    #         # return face, stop-start
    #         return face
    #     else:
    #         if self.n_landmarks==5:
    #             face=self._align_(image, bbox, points)
    #         # return face, None
    #         return face
    def align(self, image, bbox, points=None, image_size=[112, 112], margin=15):
        if points is not None:
            assert len(image_size) == 2
            src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041]], dtype=np.float32)
            if image_size[1] == 112:
                src[:, 0] += 8.0

            if isinstance(points, dict):
                dst = np.array(list(points.values()))
            else:
                dst = points.astype(np.float32)

            tform = trans.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2, :]

        if M is None:
            if bbox is None:  # use center crop
                det = np.zeros(4, dtype=np.int32)
                det[0] = int(image.shape[1] * 0.0625)
                det[1] = int(image.shape[0] * 0.0625)
                det[2] = image.shape[1] - det[0]
                det[3] = image.shape[0] - det[1]
            else:
                det = bbox
            # margin = kwargs.get('margin', 15)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2, 0)
            bb[1] = np.maximum(det[1] - margin / 2, 0)
            bb[2] = np.minimum(det[2] + margin / 2, image.shape[1])
            bb[3] = np.minimum(det[3] + margin / 2, image.shape[0])
            ret = image[bb[1]:bb[3], bb[0]:bb[2], :]
            if len(image_size) > 0:
                ret = cv2.resize(ret, (image_size[1], image_size[0]))
            # self.draw(warped)

            return ret, None, image
        else:  # do align using landmark
            assert len(image_size) == 2

            warped = cv2.warpAffine(image, M, (image_size[1], image_size[0]), borderValue=0.0)
            face, M = self.align_with_M(image, bbox, points)
            # self.draw(warped)
            return warped, M, face

    def draw(self, face):
        cv2.imshow("Faces", face)
        cv2.waitKey(0)


if __name__ == '__main__':
    face_align = FaceAligner()