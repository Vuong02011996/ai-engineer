import os
# from milvus.client.types import MetricType
import json
from pymilvus.client.types import LoadState
import ast



def connect_milvus_2_4():
    milvus_client = MilvusClient(
        uri="http://" + os.getenv("MILVUS_HOST") + ":" + str(os.getenv("MILVUS_PORT"))
    )
    # client = MilvusClient(
    #     uri="http://localhost:19530"
    # )
    collection_name = os.getenv("collection_name")
    partition_name = os.getenv("partition_name")
    return milvus_client, collection_name, partition_name

milvus_client, collection_name, partition_name = connect_milvus_2_4()

class MilvusCloverDAL(object):
    def __init__(self, collection=collection_name, partition=partition_name):
        self.collection_name = collection
        self.partition_name = partition
        self.dim = 512
        self.milvus_client = milvus_client
        self.create_collection()
        self.create_partition()

    def create_collection(self):
        # status, ok = self.milvus_client.has_collection(self.collection_name)
        # if not ok:
        #     default_collection_params = {
        #         "collection_name": self.collection_name,
        #         "dimension": self.dim,
        #         "metric_type": MetricType.IP,  # optional
        #     }
        #
        #     self.milvus_client.create_collection(default_collection_params)

        # 2. Create a collection
        # self.milvus_client.has_collection()

        res = self.milvus_client.get_load_state(
            collection_name=self.collection_name
        )

        print(" res create collection: ", res["state"])
        if res["state"] is not LoadState.Loaded:
            self.milvus_client.create_collection(
                collection_name=self.collection_name,
                dimension=self.dim,
                metric_type="IP",
                auto_id=True
            )


    def create_partition(self):
        # check if the collection is existed or not
        # status, ok = self.milvus_client.has_partition(self.collection_name, self.partition_name)
        #
        # if not ok:
        #     # create a new collection
        #     status = self.milvus_client.create_partition(self.collection_name, self.partition_name)

        res = self.milvus_client.has_partition(
            collection_name=self.collection_name,
            partition_name=self.partition_name
        )
        print("res partition: ", res)
        if res is False:
            self.milvus_client.create_partition(
                collection_name=self.collection_name,
                partition_name=self.partition_name
            )
    def insert_data(self, vectors):
        """

        :param vectors: list[list[float]], `example records: [[1.2345],[1.2345]]`
        :return:
        """
        # status, results = self.milvus_client.insert(
        #     self.collection_name, records=vectors, partition_tag=self.partition_name
        # )
        # if status.OK():
        #     return results
        # else:
        #     print("Insert milvus failed.")
        # info_collection = self.get_info_data_collection()

        # data = [
        #     {"id": 1, "vector": vectors[0]}
        # ]

        data = [
            {"vector": vectors[0]}
        ]

        res = self.milvus_client.insert(
            collection_name=self.collection_name,
            data=data,
            partition_name=self.partition_name
        )
        return res


    def search_vector(self, facial_vectors):
        """

        Args:
            facial_vectors: list vector face, each face vector have size 512 => list[N, 512]
        Returns:
            List result, each element of list is dictionary is result of each face vector; len list is N.
             [{'distance': 0.9067776501178741, 'id': 1715308191892497000}, {'distance': 0.9067776501178741, 'id': 1715308191892497000}...]
        """

        # Bulk-vector search
        res = self.milvus_client.search(
            collection_name=self.collection_name,  # Replace with the actual name of your collection
            partition_names=[self.partition_name],
            data=facial_vectors,  # Replace with your query vectors
            limit=1,  # Max. number of search results to return
            # search_params={"metric_type": "IP", "params": {}}  # Search parameters
            search_params={"metric_type": "IP", "params": {}}  # Search parameters
        )

        result = json.dumps(res, indent=4)
        result = ast.literal_eval(result)
        print(result)
        return result

        # status, results = self.milvus_client.search(
        #     self.collection_name,
        #     top_k=1,
        #     query_records=facial_vectors,
        #     partition_tags=[self.partition_name]
        #
        # )
        # if status.OK():
        #     list_results = []
        #     for entities in results:
        #         for top_k in entities:
        #             list_results.append({"id": top_k.id, "distance": 1 - top_k.distance})
        #             # list_results.append({"id": top_k.id, "distance": np.sqrt(top_k.distance)})
        #     return list_results
        # else:
        #     print("Search in milvus failed.")
        #     return []

    def get_info_data_collection(self):
        res = self.milvus_client.describe_collection(self.collection_name)
        print(res)
        return res


    def get_all_vector_in_milvus(self):
        status, collection_info = self.milvus_client.get_collection_stats(collection_name=self.collection_name)
        # print(status, collection_info)
        partition_list = collection_info["partitions"]
        for partition in partition_list:
            if partition["tag"] == self.partition_name:
                segment_list = partition["segments"]
                for segment in segment_list:
                    segment_name = segment["name"]
                    status, id_list = self.milvus_client.list_id_in_segment(collection_name=self.collection_name,
                                                                       segment_name=segment_name)
                    # print(id_list)
                    # print(status, "segment", segment_name, "has", len(id_list), "vectors")
                    return id_list



    def get_entities_by_id(self, list_id):
        """

        :param list_id: list_id = [1630142375088770000, 1630142375088770001, 1630142375088770002]
        :return:
        """
        entities = self.milvus_client.get_entity_by_id(collection_name=self.collection_name, ids=list_id)
        return entities

    def delete_entities(self, ids: list):
        self.milvus_client.delete_entity_by_id(self.collection_name, ids)
        self.milvus_client.flush([self.collection_name])


if __name__ == '__main__':
    # milvus_dal = MilvusCloverDAL()
    # milvus_client.drop_collection("identities_oryza_test")
    # milvus_client.drop_partition(collection_name, partition_name)
    # milvus_staging_dal.create_collection()
    milvus_client.drop_collection(
        collection_name=collection_name
    )