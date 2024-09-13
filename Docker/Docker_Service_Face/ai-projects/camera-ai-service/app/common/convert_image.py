import math
from skimage import transform as trans

from PIL import Image
import io
import base64
import cv2
import face_recognition
import numpy as np

def align(image, points=None):
    image_size = [112, 112]

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
    warped = cv2.warpAffine(image, M, (image_size[1], image_size[0]), borderValue=0.0)
    return warped

def convert_image(image, target_size=100):
    try:
        # Convert image bytes to NumPy array
        image_array = np.frombuffer(image, np.uint8)
        # Decode the NumPy array to an OpenCV image
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            return False

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_landmarks_list = face_recognition.face_landmarks(rgb_image)
        if len(face_landmarks_list) != 1:
            return False

        face_landmarks = face_landmarks_list[0]
        points = {
            'left_eye': np.mean(face_landmarks['left_eye'], axis=0),
            'right_eye': np.mean(face_landmarks['right_eye'], axis=0),
            'nose': np.mean(face_landmarks['nose_tip'], axis=0),
            'mouth_left': np.mean(face_landmarks['top_lip'], axis=0),
            'mouth_right': np.mean(face_landmarks['bottom_lip'], axis=0)
        }
        aligned_face = align(image, points)

        # Compress the cropped image to approximately 100KB
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, buffer = cv2.imencode(".jpg", aligned_face, encode_param)

        # Adjust quality to approximate 100KB
        target_size = target_size * 1024  # 100KB in bytes
        quality = 90
        step = 5
        while len(buffer) > target_size and quality > 0:
            quality -= step
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, buffer = cv2.imencode(".jpg", aligned_face, encode_param)

        cropped_image_bytes = buffer.tobytes()

        return cropped_image_bytes

    except Exception as e:
        print(e)
        return False


def convert_image_base64_downsize(image: bytes, target_size: int = 50):
    """
    The input image must be a bytes object.
    The output will be a base64 string with size less than 50KB.
    """
    try:
        # Open the image
        opened_image = Image.open(io.BytesIO(image))
        if opened_image.mode == "RGBA":
            opened_image = opened_image.convert("RGB")
    except Exception as e:
        raise ValueError("Cannot identify image file", e)

    original_size = len(image)

    # Calculate the ratio
    ratio = math.sqrt(target_size * 1024 / original_size)

    while True:
        # Calculate the new size
        new_size = (int(opened_image.width * ratio), int(opened_image.height * ratio))

        # Resize the image
        resized_image = opened_image.resize(new_size, Image.LANCZOS)

        # Save the image to a BytesIO object
        output = io.BytesIO()
        resized_image.save(output, format="JPEG")

        # Get the byte data
        resized_image_bytes = output.getvalue()

        # Convert the bytes to base64
        base64_image = base64.b64encode(resized_image_bytes)

        # Check the size
        if len(base64_image) <= target_size * 1024:  # target_size KB
            break

        # If the image is still too large, reduce the ratio and try again
        ratio *= 0.9

        # Save the resized image to a file in the temp directory
        with open("temp/resized_image.jpg", "wb") as f:
            f.write(resized_image_bytes)

    # Return the base64 string
    return base64_image.decode("utf-8")
