import time

# from app.app_utils.minio_utils import upload_image
from app.app_utils.file_io_untils import upload_img_from_disk
from app.mongo_dal.identity_dal import IdentityDAL
from pymongo import MongoClient
from app.milvus_dal.clover_dal import MilvusCloverDAL
from core.service.face_recognition.service_insightface_rest import extract_embedding_image_minio
from app.app_utils.face_local_utils_v2 import FaceLocalUtils


identity_dal = IdentityDAL()
milvus_staging_dal = MilvusCloverDAL()


def copy_collection_from_db_to_other_db(src_db, target_db, collection_name=""):
    db1 = MongoClient('mongodb://14.241.120.239:11037', username="root", password="example")[src_db][collection_name]
    db2 = MongoClient('mongodb://localhost:11037', username="root", password="example")[target_db][collection_name]
    # here you can put the filters you like.
    for a in db1.find():
        try:
            db2.insert(a)
            print(a)
        except Exception as e:
            print(e)
            print('did not copy')


def get_all_url_face_id_and_update_face_id():
    """
    get all url in matching_face_ids -> extract embedding -> save to milvus.
    :return:
    """
    # get all url face id using aggregation
    pipeline = [
                {"$match": {"type": 'Hoc Sinh'}}]
    # data = list(identity_dal.find_all())
    data = list(identity_dal.aggregate(pipeline))
    len_url = 0

    for hs in data[:]:
        list_url = list(map(lambda x: x['url_face'], hs["matching_face_ids"]))
        print("len list url", len(list_url))
        len_url += len(list_url)
        # start_time = time.time()
        embedding_vectors, list_img_url_filter = extract_embedding_image_minio(list_url)
        if embedding_vectors is None:
            identity_dal.delete_document([hs["_id"]])
        else:
            list_face_id = milvus_staging_dal.insert_data(embedding_vectors)
            # print(list_face_id)
            # print("extract_embedding_image_minio cost", time.time() - start_time)
            matching_face_ids = []
            for i, face_id in enumerate(list_face_id):
                matching_face_ids.append({
                    'url_face': list_img_url_filter[i],
                    "face_id": face_id
                })

            data_update = {
                "matching_face_ids": matching_face_ids,
            }
            identity_dal.update_document([hs["_id"]], [data_update])


def get_all_origin_url_and_update_face_id():
    """
    get all url in matching_face_ids -> extract embedding -> save to milvus.
    :return:
    """
    # get all url face id using aggregation
    pipeline = [
                {"$match": {"type": 'Hoc Sinh'}}]
    # data = list(identity_dal.find_all())
    data = list(identity_dal.aggregate(pipeline))
    len_url = 0

    for hs in data[:]:
        start_time = time.time()
        embedding_vectors, image_face = FaceLocalUtils().face_for_url_image(hs["original_url"])
        image_name = hs["original_url"].split("/")[-1].split(".")[0]
        # image_url = upload_image(image_face, folder_name="identities", image_name=image_name)
        image_url = upload_img_from_disk(image_name=image_name, img_arr=image_face)
        list_face_id = milvus_staging_dal.insert_data([embedding_vectors])
        print(list_face_id)
        print("extract_embedding_image_minio cost", time.time() - start_time)
        matching_face_ids = []
        for i, face_id in enumerate(list_face_id):
            matching_face_ids.append({
                'url_face': image_url,
                "face_id": face_id
            })

        data_update = {
            "matching_face_ids": matching_face_ids,
        }
        identity_dal.update_document([hs["_id"]], [data_update])


def get_vector_with_face_id(face_id=None):
    pipeline = [
        {"$match": {"type": 'Hoc Sinh'}},
        {"$project": {"_id": 0, "matching_face_ids.url": 1}}]
    data = list(identity_dal.aggregate(pipeline))

    a = 0


if __name__ == '__main__':
    # copy_collection_from_db_to_other_db(src_db="clover_staging", target_db="clover_staging", collection_name="identities")
    # get_all_origin_url_and_update_face_id()
    get_all_url_face_id_and_update_face_id()
    # identity_dal.drop_collection()
    # num_face_id = list(identity_dal.count_face_id_in_all_collection())
    # print(num_face_id)

    # test_query_and_search()
