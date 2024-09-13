import os
import traceback
from ast import literal_eval
from kthread import KThread
from datetime import datetime
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
import numpy as np
import requests
from sentry_sdk import capture_message

from app.app_utils.file_io_untils import ip_run_service_ai
from app.app_utils.identity_utils import get_matching_face_ids_and_original_url, concatenate_face_one_identity, insert_folder_video_to_sign_in_identity, get_data_matching_face_ids_v3
from app.services.services_helper import get_num_page_from_limit, get_utc_time_from_datetime, pagination
from app.mongo_dal.identity_dal import IdentityDAL
from app.milvus_dal.clover_dal import MilvusCloverDAL

blueprint = Blueprint("Identity_AI", __name__)
ns = Api(blueprint)
namespace = ns.namespace("Identity_AI")

identity_dal = IdentityDAL()
milvus_staging_dal = MilvusCloverDAL()

url_server_save_file = os.getenv("url_server_save_file")


@namespace.route("/get_identities_in_DB_AI", methods=["GET"])
class FindById(Resource):
    def get(self):
        """
         :param limit, page, branch_cam, class_cam, fromDate, toDate, user_id
        {
            "status": 200,
            "title": "Get list identity successfully.",
            "data": [
                {
                    "name": "Vuong test1",
                    "user_id": "3a015f9d-9e3e-d62c-fe18-3394ae8018a3",
                    "type": "Hoc Sinh",
                    "created_at": "2022-01-20T09:28:30Z",
                    "image_url": [
                        "https://erp-clover-file.demo.greenglobal.com.vn/file-storage/2022/01/20220120/3a0188fd-c462-a4e6-00e7-e1390ae8f12d.png",
                        "https://erp-clover-file.demo.greenglobal.com.vn/file-storage/2022/01/20220120/3a0188fd-c126-fe53-9141-090d2c0dec9d.png"
                    ]
                },
                {
                    "name": "Phong test",
                    "user_id": "3a01a625-c14c-7f0f-393c-511568f62e47",
                    "type": "Hoc Sinh",
                    "created_at": "2022-01-26T01:21:12Z",
                    "image_url": [
                        "https://erp-clover-file.demo.greenglobal.com.vn/file-storage/2022/01/20220126/3a01a625-c80e-5bfd-4dce-7639eaa1dacc.png",
                        "https://erp-clover-file.demo.greenglobal.com.vn/file-storage/2022/01/20220126/3a01a625-c589-282a-ad17-11632ad155df.png"
                    ]
                }
                            ],
            "meta": {
                "pagination": {
                    "total": 5,
                    "current_page": 1,
                    "total_pages": 1
                }
            }
            }
        :return:
        """
        limit = request.args.get('limit', default=None, type=int)
        page = request.args.get('page', default=None, type=int)
        branch_id = request.args.get('branch_id', default=None, type=str)
        class_id = request.args.get('class_id', default=None, type=str)
        user_id = request.args.get('user_id', default=None, type=str)

        item = identity_dal.find_all_item()
        new_item = []
        for identity in item:
            if "matching_face_ids" in identity and len(identity["matching_face_ids"]) > 0:
                image_url = list(map(lambda d: d['url_face'], identity["matching_face_ids"]))
            else:
                image_url = []
            identity_info = {
                "name": identity["name"] if "name" in identity else None,
                "user_id": identity["user_id"] if "user_id" in identity else None,
                "branch_id": identity["branch_id"] if "branch_id" in identity else None,
                "class_id": identity["class_id"] if "class_id" in identity else None,
                "branch_name": identity["branch_name"] if "branch_name" in identity else None,
                "class_name": identity["class_name"] if "class_name" in identity else None,
                "type": identity["type"] if "type" in identity else None,
                "created_at": get_utc_time_from_datetime(identity["created_at"]),
                "image_url": image_url,
            }
            new_item.append(identity_info)
        item = new_item

        # Filter with branch_id
        if branch_id is not None:
            new_item = []
            for hs in item:
                if hs["branch_id"] == branch_id:
                    new_item.append(hs)
            item = new_item

        # Filter with class_id
        if class_id is not None:
            new_item = []
            for hs in item:
                if hs["class_id"] == class_id:
                    new_item.append(hs)
            item = new_item

        # Filter name in list_user_id_search
        if user_id is not None and len(user_id) > 0:
            list_user_id_search = user_id.split(",")
        else:
            list_user_id_search = None
        if list_user_id_search is not None:
            new_item = []
            for hs in item:
                if hs["user_id"] in list_user_id_search:
                    new_item.append(hs)

        data_out = pagination(limit, new_item, page)

        return data_out


@namespace.route("/get_all_identities_from_dot_net", methods=["GET"])
class FindById(Resource):
    def get(self):
        """
        Gọi API lấy tất cả học sinh trên db BE về, kiểm tra user_id nào đã có trong DB AI thì không tạo mới.
        Sau khi tạo mới xong hết tất cả sẽ trả về response cho FE (loading có thể hơi lâu tầm 20s)
        Sau khi FE nhận được response sẽ tự động onLoad để show lại data mới.
        :return:
        """

        item_db_ai = identity_dal.find_all_item()
        id_students_ai = list(map(lambda d: d['user_id'], item_db_ai))
        # if dict(request.headers).get("Authorization") is not None:
        if True:
            # Get all student from database .NET
            # url_all_student = os.getenv("url_all_student")
            url_all_student = os.getenv("url_all_student")
            # dict(request.headers)["Authorization"]:
            '''
            Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE1NTIyMzNDRTU0QUE4NDQyRDVBMEQ4N0ZBQ0U1NjlGIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2NzkzODk0MTIsImV4cCI6MTcxMDkyNTQxMiwiaXNzIjoiaHR0cHM6Ly9zc28uZXJwLmNsb3Zlci5lZHUudm4iLCJhdWQiOiJFcnAiLCJjbGllbnRfaWQiOiJFcnBfQXBwIiwic3ViIjoiMzlmYzc4NWItMzk2Zi0xOGQyLTI0ZWUtNTQ3ZjMwNzk5YTgxIiwiYXV0aF90aW1lIjoxNjc5Mzg5NDEyLCJpZHAiOiJsb2NhbCIsInJvbGUiOiJhZG1pbiIsInBob25lX251bWJlcl92ZXJpZmllZCI6IkZhbHNlIiwiZW1haWwiOiJhZG1pbkBhYnAuaW8iLCJlbWFpbF92ZXJpZmllZCI6IkZhbHNlIiwibmFtZSI6ImFkbWluIiwiaWF0IjoxNjc5Mzg5NDEyLCJzY29wZSI6WyJFcnAiXSwiYW1yIjpbInB3ZCJdfQ.jLLQ9j0lmv_TMh3i5reuMSr4hgdfDalp_cVxMuaD3R0f8abOhMnBJ7fUaCOYnYz3k3hOpYyXLJf8qtNIQ_yvGLIsCh9pOlMz9Jy0Q8huj7J40WR00bUTi-akuMqOn2QDiI1ZXBNOCaJLfi2pBZam9VISEr1VsY5U6dNJXTc8_RBkP_mvQ-eMSgsHPqRz3XMS-Wt0jpvQ0dLQoyAmXpCsE3SKgQrqz67Sx426knLyGky1CSo7k49FvVaHCX4BmNMICaVGh95q5nMHdONpxqppADT-NdKsTUTay4qz64mb9o2CXe9HrJYSP-Llyn4Y1OPO3jD0aW9MNQxgUoPfBlQ6rg
            '''
            payload = {}
            headers = {
                # 'Authorization': dict(request.headers)["Authorization"]
                'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE1NTIyMzNDRTU0QUE4NDQyRDVBMEQ4N0ZBQ0U1NjlGIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2NzkzODk0MTIsImV4cCI6MTcxMDkyNTQxMiwiaXNzIjoiaHR0cHM6Ly9zc28uZXJwLmNsb3Zlci5lZHUudm4iLCJhdWQiOiJFcnAiLCJjbGllbnRfaWQiOiJFcnBfQXBwIiwic3ViIjoiMzlmYzc4NWItMzk2Zi0xOGQyLTI0ZWUtNTQ3ZjMwNzk5YTgxIiwiYXV0aF90aW1lIjoxNjc5Mzg5NDEyLCJpZHAiOiJsb2NhbCIsInJvbGUiOiJhZG1pbiIsInBob25lX251bWJlcl92ZXJpZmllZCI6IkZhbHNlIiwiZW1haWwiOiJhZG1pbkBhYnAuaW8iLCJlbWFpbF92ZXJpZmllZCI6IkZhbHNlIiwibmFtZSI6ImFkbWluIiwiaWF0IjoxNjc5Mzg5NDEyLCJzY29wZSI6WyJFcnAiXSwiYW1yIjpbInB3ZCJdfQ.jLLQ9j0lmv_TMh3i5reuMSr4hgdfDalp_cVxMuaD3R0f8abOhMnBJ7fUaCOYnYz3k3hOpYyXLJf8qtNIQ_yvGLIsCh9pOlMz9Jy0Q8huj7J40WR00bUTi-akuMqOn2QDiI1ZXBNOCaJLfi2pBZam9VISEr1VsY5U6dNJXTc8_RBkP_mvQ-eMSgsHPqRz3XMS-Wt0jpvQ0dLQoyAmXpCsE3SKgQrqz67Sx426knLyGky1CSo7k49FvVaHCX4BmNMICaVGh95q5nMHdONpxqppADT-NdKsTUTay4qz64mb9o2CXe9HrJYSP-Llyn4Y1OPO3jD0aW9MNQxgUoPfBlQ6rg"
            }
            response = requests.request("GET", url_all_student, headers=headers, data=payload)
            all_students = response.json()
            number_students = all_students["totalCount"]
            id_all_students = list(map(lambda d: d['id'], all_students["items"]))
            assert len(id_all_students) == len(all_students["items"]) == number_students

            # Kiểm tra nếu user_id trong mảng id_all_students không có trong id_students_ai của AI thì tạo mới
            # Nếu có rồi thì check trong BE có branch, class hay không nếu có update
            print("Num students in AI/BE: {}/{}".format(len(item_db_ai), number_students))

            for idx, students in enumerate(all_students["items"]):
                # chưa có trên ai thì tạo mới thôi
                if students["id"] not in id_students_ai:

                    # Kiểm tra nếu có hình ảnh khuôn mặt thì lấy vector khuôn mặt lưu vào milvus
                    if students.get("fileImage") is not None and isinstance(students["fileImage"], str):
                        data_insert = {
                            "name": students["fullName"],
                            "user_id": students["id"],
                            "type": "Hoc Sinh",
                        }

                        data = literal_eval(students["fileImage"])
                        print("Name: ", students["fullName"])
                        print("fileImage: ", data)
                        data_full_url = []
                        for url in data:
                            full_url = url_server_save_file + url
                            data_full_url.append(full_url)

                        matching_face_ids = get_matching_face_ids_and_original_url(data_full_url, update_ai=False,
                                                                                   det_threshold=0.50)
                        if matching_face_ids is not None:
                            data_insert.update({
                                "matching_face_ids": matching_face_ids,
                            })
                        if students["class"] is not None:
                            data_insert.update({
                                "branch_id": students["class"]["branchId"],
                                "class_id": students["class"]["id"],
                                "branch_name": students["class"]["branch"]["name"],
                                "class_name": students["class"]["name"],
                            })

                        identity_dal.create_one(data_insert)
                # Nếu đã có trong db AI update branch va class và các thông tin khác nếu cần.
                else:
                    if students["class"] is not None:
                        # Update branch_id and class_id of hs
                        data_update = {
                            "branch_id": students["class"]["branchId"],
                            "class_id": students["class"]["id"],
                            "branch_name": students["class"]["branch"]["name"],
                            "class_name": students["class"]["name"],
                            "created_at": datetime.now(),
                        }

                        identity_dal.update({"_id": identity_dal.find_id_by_user_id(students["id"])}, data_update)

        options = {"status": True, "status_code": 200, "message": "Đã đồng bộ xong dữ liệu học sinh trên BE và AI"}
        return options


@namespace.route("/update_identities_in_DB_AI", methods=["PUT"])
class FindById(Resource):
    def put(self):
        """Update an identity. Images field can be empty.

        - Update the name of user
        - Update the images of user
        - Update the facial data
        """
        # check _id have in mongo
        request_data = request.json
        if not request_data:
            return {"status": False, "status_code": 404, "message": "Resource not found"}

        user_id = request_data.get("user_id")
        data = request_data.get("data")
        print("user_id", user_id)
        print("data", data)
        mongo_id = identity_dal.find_one_by_condition({"user_id": user_id}, columns={"_id": 1})
        if len(data) == 0 and mongo_id is not None:
            print("Not update! data add is empty")
            options = {"status": True, "status_code": 200, "message": "Not update! data add is empty"}
            return options

        if mongo_id is not None:  # UPDATE
            mongo_id = mongo_id["_id"]
            item = identity_dal.find_by_id(mongo_id)
            user_id = user_id if user_id is not None else item["user_id"]
            try:
                data_images_saved = list(map(lambda d: d['url_ori'], item["matching_face_ids"]))
            except Exception as e:
                capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
                print(e)
                data_images_saved = []
            # Check id image update have data_images_saved
            data = list(np.setdiff1d(np.array(data), np.array(data_images_saved)))
            if len(data) == 0:
                options = {"status": True, "status_code": 200, "message": "Not update! Data url was had update"}
                print("Not update! Data url was had update")
                data_update = {
                    "user_id": user_id,
                    "created_at": datetime.now(),
                }

                identity_dal.update({"_id": mongo_id}, data_update)
                return options
            # what if the matching_face_ids did not exist
            if item.get("matching_face_ids") is None:
                matching_face_ids_current = []
            else:
                matching_face_ids_current = list(item["matching_face_ids"])

            data_full_url = []
            for url in data:
                full_url = url_server_save_file + url
                print("full_url", full_url)
                data_full_url.append(full_url)
            matching_face_ids_new = get_matching_face_ids_and_original_url(data_full_url, update_ai=False,
                                                                           det_threshold=0.5)

            if matching_face_ids_new is None:
                message = "Update identity failed! Not found any faces in image! Please upload image have face!"
                options = {"status": False, "status_code": 400, "message": message}
                return options

            data_update = {
                "user_id": user_id,
                "matching_face_ids": matching_face_ids_new + matching_face_ids_current,
                "created_at": datetime.now(),
            }

            identity_dal.update({"_id": mongo_id}, data_update)
            options = {"status": True, "status_code": 200, "message": "Identity is updated successfully"}
            return options
        else:  # REGISTER
            options = {"status": True, "status_code": 200, "message": "user_id is none"}
            return options


@namespace.route("/delete_identity_v2", methods=["PUT"])
class FindById(Resource):
    def put(self):
        """Delete url image an identity from web with url origin camera.
        Model: PUT
        {
            "user_id": "64b76ab4-ec05-44c2-9349-35bfe3b5f55c",
            "url_delete": "https://clover-file.greenglobal.com.vn/file-storage/2022/03/20220324/3a02cec5-817c-2902-572f-1480be416203.png"
        }
        """
        # check _id have in mongo
        request_data = request.json
        if not request_data:
            return {"status": False, "status_code": 404, "message": "Resource not found"}
        user_id = request_data.get("user_id")
        url_delete = request_data.get("url_delete")
        print("user_id", user_id)
        print("url_delete", url_delete)

        mongo_id = identity_dal.find_one_by_condition({"user_id": user_id}, columns={"_id": 1})
        if mongo_id is not None:  # UPDATE
            mongo_id = mongo_id["_id"]
            item = identity_dal.find_by_id(mongo_id)
            matching_face_ids = list(item["matching_face_ids"])
            # list_url = list(map(lambda d: d["url"], matching_face_ids))
            matching_face_ids_new = []
            list_face_id_delete = []
            for i in range(len(matching_face_ids)):
                if url_delete == matching_face_ids[i]["url_face"]:
                    list_face_id_delete.append(matching_face_ids[i]["face_id"])
                else:
                    matching_face_ids_new.append(matching_face_ids[i])
            if len(list_face_id_delete) > 0:
                milvus_staging_dal.delete_entities(list_face_id_delete)
                if len(matching_face_ids_new) == 0:
                    item = identity_dal.delete({"_id": mongo_id})
                else:
                    data_update = {
                        "matching_face_ids": matching_face_ids_new,
                        # "matching_face_ids": matching_face_ids_new,
                        "created_at": datetime.now(),
                    }
                    identity_dal.update({"_id": mongo_id}, data_update)
                return {"status": True, "status_code": 200, "message": "Remove image successfully"}
            else:
                return {"status": True, "status_code": 200, "message": "url_delete not found face id"}

        else:  # REGISTER
            print("Update identity failed - User_id not found in database")
            return {"status": True, "status_code": 200, "message": "User_id not found in database"}


def delete_all_identity():
    # delete all identity in milvus
    id_list = milvus_staging_dal.get_all_vector_in_milvus()
    all_students = identity_dal.find_all_item()
    list_face_id_all_st = []
    for st in all_students:
        list_face_id = list(map(lambda d: d['face_id'], st["matching_face_ids"]))
        list_face_id_all_st += list_face_id
    id_remove = np.intersect1d(np.array(id_list), np.array(list_face_id_all_st))
    if len(id_remove) > 0:
        milvus_staging_dal.delete_entities(list(map(int, id_remove)))
    identity_dal.drop_collection()

    if len(all_students) == 0 and len(id_list) > 0:
        milvus_staging_dal.delete_entities(list(map(int, id_list)))


if __name__ == '__main__':
    delete_all_identity()
