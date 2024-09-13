from flask import Blueprint, request
from flask_restx import Api, Resource
from core.main.main_utils.helper import convert_base64_to_array, read_url_img_to_array
from app.app_utils.face_local_utils_v2 import FaceLocalUtils
# from app.app_utils.minio_utils import upload_image
from app.app_utils.file_io_untils import upload_img_from_disk
from app.app_utils.face_local_utils import FaceLocalUtils as FaceLocalUtils_old
import cv2

distance_threshold = 0.8
face_util = FaceLocalUtils(distance_threshold=distance_threshold)
blueprint = Blueprint("Sign_In_Face", __name__)
ns = Api(blueprint)
namespace = ns.namespace("Sign_In_Face")


def is_match(data_input, is_base64=False):
    if is_base64:
        img_array = convert_base64_to_array(data_input)
    else:
        img_array = read_url_img_to_array(data_input)
    cv2.imwrite('/home/gg_greenlab/Pictures/color_img.jpg', img_array)
    # facial_vector, face_array, accuracy_face_detect = face_util.detect_face_and_get_embedding_an_image_scrfd(img_array)
    face_local = FaceLocalUtils_old()
    facial_vector, face_array, accuracy_face_detect = face_local.detect_face_and_get_embedding_an_image(
        img_array)

    if facial_vector is not None:
        user_id, name, min_distance = face_util.get_identity_list_facial_vector([facial_vector])
        # image_url = upload_image(face_array, folder_name="sign_in", image_name="test1")
        image_url = upload_img_from_disk(image_name="test1", img_arr=face_array)

        if name != "Unknown":
            data_out = {
                        "status": True,
                        "status_code": 200,
                        "authorized": True,
                        "user_id": user_id,
                        "message": "Valid user",
                        "name": name,
                        "threshold": distance_threshold,
                        "prediction": min_distance,
                        "url": image_url,
                    }
        else:
            data_out = {
                "status": False,
                "status_code": 404,
                "authorized": False,
                "user_id": "",
                "message": "Not found in database",
                "name": "Unknown",
                "threshold": distance_threshold,
                "prediction": min_distance,
                "url": image_url,
            }
    else:
        data_out = {
            "status": False,
            "status_code": 200,
            "authorized": False,
            "user_id": "",
            "message": "Cannot detect face in image",
            "name": "Unknown",
        }

    return data_out


@namespace.route("/verification", methods=["POST"])
class Verification(Resource):
    def post(self):
        """ Face ID Module - Get base64 image and return user_id in database
        Document: https://www.notion.so/API-Documentationadf-8a7af59e9e3349cea06e724c64c5dc69#1259f44a2018436185f2acc68df2986e
        """
        request_data = request.json
        # 1.7.5 Trường hợp không có trường image trong request
        if request_data.get("image") is None:
            options = {
                "status": False,
                "status_code": 404,
                "authorized": False,
                "user_id": "",
                "name": "Unknown",
                "message": "Image field was not found",
                "sent_data": request_data,
            }
            return options

        data_input = request_data["image"]
        if len(data_input) == 0:
            options = {
                "status": False,
                "status_code": 404,
                "authorized": False,
                "user_id": "",
                "name": "Unknown",
                "message": "Content was not found in image field",
                "sent_data": request_data,
            }
            return options

        if request_data.get("type") == "url":
            return is_match(data_input, is_base64=False)
        else:
            return is_match(data_input, is_base64=True)


