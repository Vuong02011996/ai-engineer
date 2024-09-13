import base64
import traceback
from datetime import datetime
from io import BytesIO
import numpy as np
from PIL import Image
import pyheif
import cv2
import requests
from sentry_sdk import capture_message
from skimage import transform as trans
import secrets
import string

# from app.mongo_dal.camera_dal import CameraDAL
# from app.mongo_dal.process_dal import ProcessDAL
from skimage import io

from app.app_utils.file_io_untils import upload_img_from_disk, get_url_from_array_image_to_file_server, \
    ip_run_service_ai


# process_dal = ProcessDAL()
# camera_dal = CameraDAL()


def convert_base64_to_array(img_base64):
    """ Convert the base64 string image to numpy array """
    base64_img_bytes = img_base64.encode("utf-8")
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    return cv2.imdecode(np.frombuffer(decoded_image_data, dtype="uint8"), 1)


def convert_np_array_to_base64(image):
    """

    :param image: np array image
    :return: string image base64
    """
    success, encoded_image = cv2.imencode('.jpg', image)
    image_face = encoded_image.tobytes()
    image_base64 = base64.b64encode(image_face).decode('ascii')
    return image_base64


def file2base64(path):
    """
    :param path: path image
    :return: string base64 image
    """
    with open(path, mode='rb') as fl:
        encoded = base64.b64encode(fl.read()).decode('ascii')
        return encoded


def get_url_as_base64(url):
    """
    :param url: url image
    :return: string base64 image
    """
    img = base64.b64encode(requests.get(url).content).decode('ascii')
    return img


def read_url_img_to_array(url):
    if url[-4:] == "HEIC":
        response = requests.get(url)
        bytesIo = response.content
        i = pyheif.read(bytesIo)
        pi = Image.frombytes(
            mode=i.mode, size=i.size, data=i.data)
        img = np.array(pi)
        """Không cần resize vì qua model đã resize(1000, 1000)"""

    # response = requests.get(url)
    # img = Image.open(BytesIO(response.content))
    # img = np.array(img)
    # https://pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
    else:
        try:
            img = io.imread(url)
        except Exception as e:
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
            print("Lỗi đọc ảnh từ url: ", e)
            print("url: ", url)
            img = None
    return img


def align_face(img, bbox, landmark):
    """Align the face based on the landmark and bounding boxes

    Args:
        img (np.array): raw image(image array)
        bbox (list): bounding box list [7, 136, 254, 435]
        landmark (): [[ 73.44393 317.95898]
                      [181.28801 319.50546]
                      [124.91697 407.58472]
                      [ 98.57333 412.7461 ]
                      [168.9716  417.21915]]

    Returns:
        warped (np.array): aligned face with the shape of (112,112)
    """
    image_size = [112, 112]

    M = None
    if landmark is not None:
        src = np.array(
            [
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041],
            ],
            dtype=np.float32,
        )

        src[:, 0] += 8.0
        dst = landmark.astype(np.float32)

        tform = trans.SimilarityTransform()
        tform.estimate(dst, src)
        M = tform.params[0:2, :]
    # M: The translation, rotation, and scaling matrix.
    if M is None:
        det = bbox
        margin = 44
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - margin / 2, 0)
        bb[1] = np.maximum(det[1] - margin / 2, 0)
        bb[2] = np.minimum(det[2] + margin / 2, img.shape[1])
        bb[3] = np.minimum(det[3] + margin / 2, img.shape[0])
        ret = img[bb[1] : bb[3], bb[0] : bb[2], :]

        ret = cv2.resize(ret, (image_size[1], image_size[0]))
        return ret
    else:
        # do align using landmark
        warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)
        return warped


def align_with_M(image, bbox, points):

    bbx, bby, bbw, bbh = bbox
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


def align_face_anyshape(img, bbox, landmark, w=112, h=112):
    """Align the face based on the landmark and bounding boxes

    Args:
        img (np.array): raw image(image array)
        bbox (list): bounding box list [7, 136, 254, 435]
        landmark (): [[ 73.44393 317.95898]
                      [181.28801 319.50546]
                      [124.91697 407.58472]
                      [ 98.57333 412.7461 ]
                      [168.9716  417.21915]]

    Returns:
        warped (np.array): aligned face with the shape of (112,112)
    """
    image_size = [w, h]

    M = None
    if landmark is not None:
        src = np.array(
            [
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041],
            ],
            dtype=np.float32,
        )

        src[:, 0] += 8.0
        dst = landmark.astype(np.float32)

        tform = trans.SimilarityTransform()
        tform.estimate(dst, src)
        M = tform.params[0:2, :]
    # M: The translation, rotation, and scaling matrix.
    if M is None:
        det = bbox
        margin = 44
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0] - margin / 2, 0)
        bb[1] = np.maximum(det[1] - margin / 2, 0)
        bb[2] = np.minimum(det[2] + margin / 2, img.shape[1])
        bb[3] = np.minimum(det[3] + margin / 2, img.shape[0])
        ret = img[bb[1] : bb[3], bb[0] : bb[2], :]

        ret = cv2.resize(ret, (image_size[1], image_size[0]))
        return ret
    else:
        # do align using landmark
        warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)
        return warped


def read_image_url_reshape_and_to_base64(url):
    """
    :param url: url image
    :return: string image base64 with shape (112, 112)
    """
    img_array = read_url_img_to_array(url)
    # filter identity
    # https://stackoverflow.com/questions/63592160/preprocessing-methods-for-face-recognition-in-python
    # https://github.com/1adrianb/face-alignment
    # https://link.springer.com/article/10.1007/s11554-021-01107-w
    h, w, _ = img_array.shape
    print("h, w: ", h, w)
    if img_array is not None and w > 50 and h > 50:
        image_face = cv2.resize(img_array, (112, 112), interpolation=cv2.INTER_AREA)
        image_face = cv2.cvtColor(image_face, cv2.COLOR_BGR2RGB)
        face_base64 = convert_np_array_to_base64(image_face)
        return face_base64
    else:
        print("*******************************Filter url********************************************")
        return None


def get_url_image_person_from_box_head(box, frame_rgb):
    """
    Hàm này dùng để lấy url ảnh của person dựa trên cái đầu
    :param box: Bouding box của head là tọa độ gồm 2 điểm [x1, y1, x2, y2]
    :param frame_rgb:
    :return:
    """
    try:
        box = list(map(int, box))
        image_head = frame_rgb[box[1]:box[3], box[0]:box[2]]
        image_head = cv2.cvtColor(image_head, cv2.COLOR_BGR2RGB)
    except Exception as e:
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        print("Lỗi image_face, image face is null", "image face is null ", e)
        return None
    url_image_head = get_url_from_array_image_to_file_server(image_head)
    return url_image_head


def get_url_image_from_frame_rgb(frame_rgb):
    try:
        image = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2RGB)
    except Exception as e:
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        print("Lỗi image_face, image face is null", "image face is null ", e)
        return None
    url_image = get_url_from_array_image_to_file_server(image)
    return url_image


def generate_random_key(length=24):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


if __name__ == '__main__':
    origin_url = 'https://minio.core.greenlabs.ai/local/avatar/awazzmu27uf8is4jiiub2dmxcxjyx9.jpg'
    img_base64 = get_url_as_base64(url=origin_url)
    print(img_base64)