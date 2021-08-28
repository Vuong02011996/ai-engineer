from milvus import Milvus
from milvus.client.types import MetricType

host = "192.168.1.8"
port = 8010
milvus_client = Milvus(host, port)


class CloverDAL(object):
    def __init__(self, collection_name, partition_name):
        self.collection_name = collection_name
        self.partition_name = partition_name
        self.dim = 512
        self.milvus_client = milvus_client
        self.create_collection()
        self.create_partition()

    def create_collection(self):
        status, ok = self.milvus_client.has_collection(self.collection_name)
        if not ok:
            default_collection_params = {
                "collection_name": self.collection_name,
                "dimension": self.dim,
                "metric_type": MetricType.L2,  # optional
            }

            self.milvus_client.create_collection(default_collection_params)

    def create_partition(self):
        # check if the collection is existed or not
        status, ok = self.milvus_client.has_partition(self.collection_name, self.partition_name)

        if not ok:
            # create a new collection
            status = self.milvus_client.create_partition(self.collection_name, self.partition_name)

    def insert_data(self, vectors):
        """

        :param vectors: list[list[float]], `example records: [[1.2345],[1.2345]]`
        :return:
        """
        res = self.milvus_client.insert(
            self.collection_name, records=vectors, partition_tag=self.partition_name
        )
        if res[0].code == 0:
            return res[1]
        else:
            print("Insert milvus failed.")

    def search_vector(self, facial_vectors):
        results = self.milvus_client.search(
            self.collection_name,
            top_k=5,
            query_records=facial_vectors,
            partition_tags=[self.partition_name]

        )
        list_results = []

        # for entities in results:
        #     for top_k in entities:
        #         list_results.append({"id": top_k.id, "distance": top_k.distance})

        # print(results)

    def get_all_vector_in_milvus(self):
        status, collection_info = self.milvus_client.get_collection_stats(collection_name=self.collection_name)
        print(status, collection_info)
        partition_list = collection_info["partitions"]
        for partition in partition_list:
            if partition["tag"] == "_default":
                segment_list = partition["segments"]
                for segment in segment_list:
                    segment_name = segment["name"]
                    status, id_list = self.milvus_client.list_id_in_segment(collection_name=self.collection_name,
                                                                       segment_name=segment_name)
                    print(id_list)
                    print(status, "segment", segment_name, "has", len(id_list), "vectors")
                    return id_list

    def get_entities_by_id(self, list_id):
        """

        :param list_id: list_id = [1630142375088770000, 1630142375088770001, 1630142375088770002]
        :return:
        """
        entities = self.milvus_client.get_entity_by_id(collection_name=self.collection_name, ids=list_id)
        return entities


if __name__ == '__main__':
    milvus_staging_dal = CloverDAL(collection_name="clover_staging", partition_name="identities_hocsinh")
    milvus_staging_dal.create_collection()