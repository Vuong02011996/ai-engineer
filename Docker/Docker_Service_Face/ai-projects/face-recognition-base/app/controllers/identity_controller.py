import os
from datetime import datetime
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
import numpy as np
import requests
import uuid


from app.app_utils.identity_utils import get_matching_face_ids_ver_oryza
from app.services.services_helper import get_num_page_from_limit, get_utc_time_from_datetime, pagination
from app.mongo_dal.identity_dal import IdentityDAL
from app.milvus_dal.clover_dal import MilvusCloverDAL

blueprint = Blueprint("Identity", __name__)
ns = Api(blueprint)
namespace = ns.namespace("Identity")

identity_dal = IdentityDAL()
milvus_staging_dal = MilvusCloverDAL()

url_server_save_file = os.getenv("url_server_save_file")


@namespace.route("/register", methods=["GET", "POST"])
class FindAll(Resource):
    """ Register a new identity """
    def post(self):
        """Upload new identity to server.
        :param json file
        Example
       {
            "name": "Vuong",
            # "user_id": "64b76ab4-ec05-44c2-9349-35bfe3b5f55c",
            "type": "Nhan vien",
            "data": [
                "/home/oryza/Pictures/Face/Vuong.jpeg"
            ]
        }
        Returns: {"user_id": user_id, "status": True, "status_code": 200, "message": "Register successfully!"}
        """
        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options

        username = request_data.get("name")
        user_id = str(uuid.uuid4())
        data = request_data.get("data")
        status = request_data.get("status")
        types = request_data.get("type")
        print("username: ", username)
        print("user_id: ", user_id)
        print("data: ", data)
        print("types: ", types)

        if None in (username, user_id):
            options = {"status": False, "status_code": 404, "message": "Don't enough fields to register new user"}
            return options
        matching_face_ids = None
        if data is not None and len(data) > 0:
            matching_face_ids = get_matching_face_ids_ver_oryza(data)
            if matching_face_ids is None:
                print("Register with no data face!!")
                options = {"status": True, "user_id": user_id, "status_code": 200, "message": "Register with no data face"}
            else:
                print("Register successfully!")
                options = {"user_id": user_id, "status": True, "status_code": 200, "message": "Register successfully!"}
        else:
            print("Register with no data face!!")
            options = {"status": True, "user_id": user_id, "status_code": 200, "message": "Register with no data face"}

        identity_dal.create_one(
            {
                "name": username,
                "user_id": user_id,
                "type": types,
                "status": status,
                "matching_face_ids": matching_face_ids,
                "created_at": datetime.now(),
            }
        )
        return options


@namespace.route("/user_id/<_id>", methods=["GET", "DELETE"])
class FindById(Resource):
    def get(self, _id):
        """

        Methods GET http://192.168.111.98:30000/api/identities/user_id/c481d7d8-ba3c-438c-806e-d1c0e9e4e9f4
        Args:
            _id: user_id

        Returns:
            info user

        """
        info_user = identity_dal.find_one_by_condition({"user_id": _id}, columns={"_id": 1})
        if info_user is None:
            options = {"user_id": _id, "message": "User id is not found"}
            return options
        else:
            mongo_id = info_user["_id"]
            item = identity_dal.find_by_id(mongo_id)
            data_user = {
                "name": item["name"],
                "user_id": item["user_id"],
                "type": item["type"],
                "matching_face_ids": item["matching_face_ids"],
            }
            return data_user

    def delete(self, _id):
        """
        Delete an identity in mongo DB and its facial data in Milvus DB.
        Args:
            _id: user_id

        Returns:
            user_id deleted
        """
        info_user = identity_dal.find_one_by_condition({"user_id": _id}, columns={"_id": 1})
        if info_user is None:
            options = {"user_id": _id, "message": "User id is not found"}
            return options
        else:
            mongo_id = info_user["_id"]
        item = identity_dal.find_by_id(mongo_id)
        if item is None:
            options = {"user_id": _id, "message": "Identity is not found"}
            return options
        if item["matching_face_ids"] is None:
            item = identity_dal.delete({"_id": mongo_id})
            options = {"user_id": _id, "message": "User haven't vector face, Identity is deleted successfully"}
            return options
        else:
            matching_face_ids = list(item["matching_face_ids"])
            milvus_staging_dal.delete_entities(list(map(lambda d: d["face_id"], matching_face_ids)))

            item = identity_dal.delete({"_id": mongo_id})
            options = {"user_id": _id, "message": "Identity is deleted successfully"}
            return options


@namespace.route("/update", methods=["PUT"])
class FindById(Resource):
    def put(self):
        """Update an identity. data field can be empty.
        PUT method
        {
            "name": "Vuong_update",
            "user_id": "12f19f52-ee8b-4f14-a491-9c11198d2763",
            "type": "Nhan vien",
            "data": ["/home/oryza/Pictures/Face/Vuong.jpeg"]
        }
        """
        # check _id have in mongo
        request_data = request.json
        if not request_data:
            return {"status": False, "status_code": 404, "message": "Resource not found"}

        username = request_data.get("name")
        user_id = request_data.get("user_id")
        data = request_data.get("data")
        types = request_data.get("type")
        print("username: ", username)
        print("user_id: ", user_id)
        print("data: ", data)
        print("types: ", types)
        if None in (user_id, data):
            options = {"status": False, "status_code": 404, "message": "Don't have user_id, data to update new user"}
            return options

        info_user = identity_dal.find_one_by_condition({"user_id": user_id}, columns={"_id": 1})

        if info_user is not None:
            mongo_id = info_user["_id"]
            item = identity_dal.find_by_id(mongo_id)
            if item is None:
                options = {"status": True, "status_code": 200, "message": "mongo_id of info_user not found"}
                print("mongo_id of info_user not found")
                return options

            username = username if username is not None else item["name"]
            user_id = user_id if user_id is not None else item["user_id"]
            types = types if types is not None else item["type"]

            # delete all face_ids in milvus
            if item.get('matching_face_ids') is not None:
                matching_face_ids = list(item["matching_face_ids"])
                milvus_staging_dal.delete_entities(list(map(lambda d: d["face_id"], matching_face_ids)))
            else:
                print("Delete face in milvus but matching_face_ids not found in info user")

            # If data update haven't url face
            if len(data) == 0:
                data_update = {
                    "name": username,
                    "user_id": user_id,
                    "type": types,
                    "matching_face_ids": None,
                    "created_at": datetime.now(),
                }

                identity_dal.update({"_id": mongo_id}, data_update)
                print("Update with no url face in data")
                options = {"status": True, "status_code": 200, "message": "Update with no url face in data"}
                return options
            else:
                matching_face_ids_new = get_matching_face_ids_ver_oryza(data)
                # If data update have url face but no detect face
                if matching_face_ids_new is None:
                    data_update = {
                        "name": username,
                        "user_id": user_id,
                        "type": types,
                        "matching_face_ids": None,
                        "created_at": datetime.now(),
                    }

                    identity_dal.update({"_id": mongo_id}, data_update)
                    print("Update with url face in data no detect face")
                    options = {"status": True, "status_code": 200, "message": "Update with url face in data no detect face"}
                    return options
                else:
                    data_update = {
                        "name": username,
                        "user_id": user_id,
                        "type": types,
                        "matching_face_ids": matching_face_ids_new,
                        "created_at": datetime.now(),
                    }

                    identity_dal.update({"_id": mongo_id}, data_update)
                    options = {"status": True, "status_code": 200,
                               "message": "Update with url face in data have face"}
                    return options
        else:
            options = {"status": True, "status_code": 200, "message": "user_id is not in database, no update"}
            return options


@namespace.route("/get_all_identities_in_DB_AI", methods=["GET"])
class FindById(Resource):
    def get(self):
        """
         :param limit, page, user_id
        {
            "status": 200,
            "title": "Get list identity successfully.",
            "data": [
                {
                    "name": "Vuong",
                    "user_id": "3a015f9d-9e3e-d62c-fe18-3394ae8018a3",
                    "type": "Hoc Sinh",
                    "created_at": "2022-01-20T09:28:30Z",
                    "image_url": []
                },
                {
                    "name": "Tuan",
                    "user_id": "3a01a625-c14c-7f0f-393c-511568f62e47",
                    "type": "Hoc Sinh",
                    "created_at": "2022-01-26T01:21:12Z",
                    "image_url": [
                }
                            ]
            }
        :return:
        """

        item = identity_dal.find_all_item()
        data_out = []
        for identity in item:
            if identity["matching_face_ids"] is not None and len(identity["matching_face_ids"]) > 0:
                url_ori = list(map(lambda d: d['url_ori'], identity["matching_face_ids"]))
            else:
                url_ori = []
            identity_info = {
                "name": identity["name"] if "name" in identity else None,
                "user_id": identity["user_id"] if "user_id" in identity else None,
                "type": identity["type"] if "type" in identity else None,
                "created_at": get_utc_time_from_datetime(identity["created_at"]),
                "url_ori": url_ori,
            }
            data_out.append(identity_info)
        return data_out


def check_identities_in_DB_AI():
    # Get all vector in milvus
    milvus_dal = MilvusCloverDAL()
    id_list = milvus_dal.get_all_vector_in_milvus()
    print("id_list: ", id_list)

    item = identity_dal.find_all_item()
    data_out = []
    for identity in item:
        if identity["matching_face_ids"] is not None and len(identity["matching_face_ids"]) > 0:
            url_ori = list(map(lambda d: d['url_ori'], identity["matching_face_ids"]))
            face_id = list(map(lambda d: d['face_id'], identity["matching_face_ids"]))
            sub_list = set(face_id).issubset(set(id_list))
            if not sub_list:
                a = 0
        else:
            url_ori = []
        identity_info = {
            "name": identity["name"] if "name" in identity else None,
            "user_id": identity["user_id"] if "user_id" in identity else None,
            "type": identity["type"] if "type" in identity else None,
            "created_at": get_utc_time_from_datetime(identity["created_at"]),
            "url_ori": url_ori,
        }
        data_out.append(identity_info)
    return data_out


def combine_vector_url_in_mongo_not_in_milvus():
    """
    Get all face_id in mongo DB, if face_id not in milvus must combine all url of user to milvus
    Returns:

    """
    item = identity_dal.find_all_item()
    milvus_dal = MilvusCloverDAL()
    for identity in item:
        if identity["matching_face_ids"] is not None and len(identity["matching_face_ids"]) > 0:
            # if identity["name"] == "Hoàng Quang Linh":
            url_ori = list(map(lambda d: d['url_ori'], identity["matching_face_ids"]))
            face_id = list(map(lambda d: d['face_id'], identity["matching_face_ids"]))
            # check face_id from mongo but not in milvus
            # list_id = [face_id]
            # Delete all vector in milvus
            milvus_dal.delete_entities(face_id)

            # Update matching_face_ids in all user
            mongo_id = identity["_id"]
            matching_face_ids_new = get_matching_face_ids_ver_oryza(url_ori)
            # If data update have url face but no detect face
            if matching_face_ids_new is None:
                data_update = {
                    "matching_face_ids": None,
                    "created_at": datetime.now(),
                }

                identity_dal.update({"_id": mongo_id}, data_update)
                print("Update with url face in data no detect face")
            else:
                data_update = {
                    "matching_face_ids": matching_face_ids_new,
                    "created_at": datetime.now(),
                }

                identity_dal.update({"_id": mongo_id}, data_update)


if __name__ == '__main__':
    combine_vector_url_in_mongo_not_in_milvus()




