import random
import time

import numpy as np
import os
from milvus import Milvus
from milvus.client.types import MetricType

host = "192.168.1.8"
port = 8010
milvus_client = Milvus(host, port)

dim = 512
collection_name = "clover_staging"


def create_collection():
    default_collection_params = {
                "collection_name": collection_name,
                "dimension": dim,
                "metric_type": MetricType.L2,  # optional
            }

    milvus_client.create_collection(default_collection_params)


def insert_data(vectors):

    res = milvus_client.insert(
        collection_name, records=vectors
    )
    print(res)


def search_vector(facial_vectors):
    results = milvus_client.search(
        collection_name,
        top_k=1,
        query_records=facial_vectors,
        partition_tags=["identities_hocsinh"]
    )
    list_results = []

    # for entities in results:
    #     for top_k in entities:
    #         list_results.append({"id": top_k.id, "distance": top_k.distance})

    # print(results)


def get_all_vector_in_milvus():
    status, collection_info = milvus_client.get_collection_stats(collection_name=collection_name)
    print(status, collection_info)
    partition_list = collection_info["partitions"]
    for partition in partition_list:
        if partition["tag"] == "_default":
            segment_list = partition["segments"]
            for segment in segment_list:
                segment_name = segment["name"]
                status, id_list = milvus_client.list_id_in_segment(collection_name=collection_name,
                                                                   segment_name=segment_name)
                print(id_list)
                print(status, "segment", segment_name, "has", len(id_list), "vectors")
                return id_list


def get_entities_by_id():
    list_id = [1630142375088770000, 1630142375088770001, 1630142375088770002]
    entities = milvus_client.get_entity_by_id(collection_name=collection_name, ids=list_id)
    start_time = time.time()

    results = milvus_client.search(
        collection_name,
        top_k=1,
        query_records=[entities[1][0]]
    )
    print(results)
    print("search cost", time.time() - start_time)


if __name__ == '__main__':
    # milvus_client.drop_collection(collection_name)
    nb = 3000
    data_string = ["test"] * 3000
    vectors = [[random.random() for _ in range(dim)] for _ in range(nb)]
    # create_collection()
    # insert_data(vectors)
    i = 0
    total_time = 0
    while i < 100:
        start_time = time.time()
        search_vector(vectors[-5:])
        print("search cost", time.time() - start_time)
        total_time += time.time() - start_time
        i +=1
    print(total_time/100)
    # get_all_vector_in_milvus()
    # start_time = time.time()
    # get_entities_by_id()
    # print("search cost", time.time() - start_time)
