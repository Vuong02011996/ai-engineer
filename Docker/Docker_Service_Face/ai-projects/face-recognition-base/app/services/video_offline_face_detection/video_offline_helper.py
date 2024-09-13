from app.app_utils.file_io_untils import ip_run_service_ai
from app.milvus_dal.clover_dal import MilvusCloverDAL
from app.mongo_dal.face_search_dal import FaceSearchDAL
from app.app_utils.extract_face_vector import ExtractVector
from core.main.main_utils.helper import read_url_img_to_array
from connect_db import connect_milvus
from datetime import datetime
import time
import pika
import os
import traceback
import json
from sentry_sdk import capture_message
from bson import ObjectId


milvus_client, collection_name, partition_name = connect_milvus()


ip_rabbitMQ_server = os.getenv("ip_rabbitMQ_server")
port_rabbitMQ_server = int(os.getenv("port_rabbitMQ_server"))


def create_database_from_black_list(black_list, partition_names, table_face_search):
    print("Process Blacklist ... save face search to db")
    list_facial_vector = []
    list_accuracy_face_detect = []
    list_image_url_ori = []
    face_utils = ExtractVector()
    for i, url in enumerate(black_list):
        img_array = read_url_img_to_array(url)
        facial_vector, face_array, accuracy_face_detect = face_utils.detect_face_and_get_embedding_an_image(img_array)
        list_facial_vector.append(facial_vector)
        list_accuracy_face_detect.append(accuracy_face_detect)
        list_image_url_ori.append(url)

        """save vector to milvus, id, url to mongo"""

    delete_data_face_search(partition_names, table_face_search)

    milvus_dal = MilvusCloverDAL(collection=collection_name, partition=partition_names)
    # face_search_dal = FaceSearchDAL()
    face_search_dal = FaceSearchDAL(collection_name=table_face_search)

    list_face_id = milvus_dal.insert_data(list_facial_vector)
    matching_face_ids = []
    for i, face_id in enumerate(list_face_id):
        matching_face_ids.append({
            # 'url_face': list_image_url[i],
            "face_id": face_id,
            "accuracy_face_detect": list_accuracy_face_detect[i],
            "url_ori": list_image_url_ori[i],
        })
        username = str(ObjectId())
        face_search_dal.create_one(
            {
                "name": username,
                "user_id": "user_id",
                "type": "types",
                "status": "status",
                "matching_face_ids": matching_face_ids,
                "created_at": datetime.now(),
            }
        )
        matching_face_ids = []

    return milvus_dal, face_search_dal


def delete_data_face_search(partition_names, table_face_search):
    milvus_client.drop_partition(collection_name, partition_names)
    # face_search_dal = FaceSearchDAL()
    face_search_dal = FaceSearchDAL(collection_name=table_face_search)
    face_search_dal.drop_collection()


def sent_data_with_rabbit_mq(data_send, channel_send_data):
    start_time = time.time()
    try:
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=ip_rabbitMQ_server, port=port_rabbitMQ_server,
                                      credentials=credentials))

        channel = connection.channel()
        channel.exchange_declare(exchange=channel_send_data,
                                 exchange_type='fanout')
        message = json.dumps(data_send)
        # pikaPublisher.send_message(data=data_send, exchange_name='FACE_RECOGNITION_EXCHANGES')
        channel.basic_publish(exchange=channel_send_data, routing_key='',
                              body=message)
        print("data send: ", data_send)
        print("Sent data to rabbitMQ cost: ", time.time() - start_time)
        connection.close()

    except Exception as e:
        print("Connect to ip_rabbitMQ_server error: IP, Port:", ip_rabbitMQ_server,
              port_rabbitMQ_server)
        capture_message(
            f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")


if __name__ == '__main__':
    partition_names = table_face_search = "face_search_66bc868e2d3cb25b095ba9ac"
    delete_data_face_search(partition_names, table_face_search)