import traceback
from datetime import datetime

from sentry_sdk import capture_message

from app.milvus_dal.clover_dal import MilvusCloverDAL
from app.mongo_dal.base_dal import BaseDAL
from app.mongo_models.face_search import FaceSearch


class FaceSearchDAL(BaseDAL):
    def __init__(self, collection_name="face_search"):
        # super().__init__(FaceSearch)
        FaceSearch.set_collection_name(collection_name)
        super().__init__(FaceSearch)

    def count_face_id_in_all_collection(self):
        pipeline_count = [
            {"$unwind": '$matching_face_ids'},
            {"$count": 'total_face_ids'}
        ]
        return self.aggregate(pipeline_count)

    def find_identity_info_with_face_id(self, face_id):
        pipeline = [
            {"$match": {"matching_face_ids.face_id": face_id}},
            {"$unwind": '$matching_face_ids'},
            {"$match": {"matching_face_ids.face_id": face_id}},
        ]
        data = list(self.aggregate(pipeline))
        # chỉ sử dụng khi đăng kí khuôn mặt có url face
        # url_match = data[0]["matching_face_ids"]["url_face"][0]
        url_match = "None"
        """
        Lỗi:     url_match = data[0]["matching_face_ids"]["url_face"],
                IndexError: list index out of range, do vector trên milvus có mà mongoDB không có.
        """
        try:
            identity_id = data[0]["_id"]
            name = data[0]["name"]

        except Exception as e:
            # print("Vector trên milvus có mà mongoDB không có")
            identity_id = None
            name = None
        return name, url_match, identity_id
        # return data[0]["name"], None, identity_id

    def find_identity_info_with_face_id_for_group(self, face_id):
        pipeline = [
            {"$match": {"matching_face_ids.face_id": face_id}},
            {"$unwind": '$matching_face_ids'},
            {"$match": {"matching_face_ids.face_id": face_id}},
        ]
        data = list(self.aggregate(pipeline))
        url_match = data[0]["matching_face_ids"]["url_face"],
        user_id = data[0]["user_id"]
        return data[0]["name"], url_match[0], user_id

    def find_id_by_user_id(self, user_id):
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def search_identity_object_by_face_ids(self, face_id):
        pipeline = [
            {"$match": {"matching_face_ids.face_id": face_id}},
            {"$unwind": '$matching_face_ids'},
            {"$match": {"matching_face_ids.face_id": face_id}},
        ]
        data = list(self.aggregate(pipeline))
        return data

    def get_all_data_face_ids(self):
        pipeline = [
            {"$unwind": '$matching_face_ids'},
        ]
        data = list(self.aggregate(pipeline))
        return data

    def check_face_id_mongo_with_milvus(self):
        # Get all vector in milvus
        milvus_dal = MilvusCloverDAL()
        id_list = milvus_dal.get_all_vector_in_milvus()
        print("id_list: ", id_list)

        # Get all vector in mongo
        data = self.get_all_data_face_ids()
        for item in data:
            face_id = item['matching_face_ids']['face_id']
            if face_id not in id_list:
                print("item['matching_face_ids']", item['matching_face_ids'])
        face_ids = [item['matching_face_ids']['face_id'] for item in data]
        print(face_ids)

        print("data: ", data)
        for face_id in id_list:
            identity = self.search_identity_object_by_face_ids(face_id)
            print(identity)


if __name__ == '__main__':
    identity_dal = IdentityDAL()
    total_face_ids = identity_dal.count_face_id_in_all_collection()
    print(list(total_face_ids)[0])
    identity_dal.check_face_id_mongo_with_milvus()

    # identity_dal.drop_collection()