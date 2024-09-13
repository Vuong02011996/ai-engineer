import cv2
import face_recognition
import numpy as np
from fastapi import HTTPException

prefix = cv2.data.haarcascades
face_cascade = cv2.CascadeClassifier(prefix + 'haarcascade_frontalface_default.xml')

def check_one_face(contents):
    try:
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            x = left
            y = top
            w = right - left
            h = bottom - top
            x -= int(w * 0.3)
            y -= int(h * 0.3)
            w += int(w * 0.6)
            h += int(h * 0.6)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if w > image.shape[1]:
                w = image.shape[1]
            if h > image.shape[0]:
                h = image.shape[0]
            crop = image[y:y + h, x:x + w]
            image = compress_image_to_size(crop, 100)
            return crop
        else:
            raise HTTPException(status_code=400, detail={"code": "4536", "message": "Image is not valid"})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail={"code": "4536", "message": "Image is not valid 2"})


def check_one_face_opencv(contents):
    try:
        # check size image
        # print(len(contents))
        # if (len(contents)/1000) < 100:
        #     nparr = np.frombuffer(contents, np.uint8)
        #     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        #     return image

        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imwrite("test.jpg", image)
        # print(len(faces))
        if len(faces) == 1:
            x, y, w, h = faces[0]
            x -= int(w * 0.3)
            y -= int(h * 0.3)
            w += int(w * 0.6)
            h += int(h * 0.6)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if w > image.shape[1]:
                w = image.shape[1]
            if h > image.shape[0]:
                h = image.shape[0]
            crop = image[y:y + h, x:x + w]
            image = compress_image_to_size(crop, 100)
            return crop
        else:
            raise HTTPException(status_code=400, detail={"code": "4536", "message": "Image is not valid"})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "4536", "message": "Image is not valid"})


def compress_image_to_size(image, target_size_kb, step=5, max_iter=100):
    target_size = target_size_kb * 1024  # Chuyển đổi KB sang bytes
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]  # Chất lượng ban đầu là 100

    for i in range(max_iter):
        is_success, buffer = cv2.imencode('.jpg', image, encode_param)
        if not is_success:
            raise ValueError("Could not encode image")

        size = len(buffer)
        if size <= target_size:
            return buffer

        encode_param[1] -= step
        if encode_param[1] < 0:
            raise ValueError("Could not compress image to the desired size")

    raise ValueError("Reached maximum iterations without achieving desired size")
