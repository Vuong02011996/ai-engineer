import time

from pymilvus_orm import Collection, CollectionSchema, FieldSchema, DataType, list_collections, connections, \
    get_connection, utility


class CloverDAL(object):
    def __init__(self, collection_name, partition_name):
        self.collection_name = collection_name
        self.partition_name = partition_name
        self.primary_name = "face_id"
        self.embedding_vector_field = "embedding_vector"
        self.collection = self.create_collection()

    def create_collection(self):
        list_collection = list_collections()
        if self.collection_name in list_collection:
            collection = Collection(name=self.collection_name)
        else:
            pk_face_id = FieldSchema(name=self.primary_name, dtype=DataType.INT64, is_primary=True, auto_id=True)
            field = FieldSchema(name=self.embedding_vector_field, dtype=DataType.FLOAT_VECTOR, dim=512)
            schema = CollectionSchema(fields=[pk_face_id, field], description="clover_staging collection")
            collection = Collection(name=self.collection_name, schema=schema)

        if self.partition_name is not None and collection.has_partition(self.partition_name) is False:
            collection.create_partition(self.partition_name)

        return collection

    def insert_entities(self, vectors):
        entities = [
            vectors
        ]
        mr = self.collection.insert(data=entities, partition_name=self.partition_name)
        utility.get_connection().flush([self.collection_name])
        print("num_entities: ", self.collection.num_entities)
        return mr.primary_keys, self.collection.num_entities

    def search_one_vector(self, vectors, limit=3):
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        # self.collection.load()

        # start_time = time.time()
        results = self.collection.search(vectors, anns_field=self.embedding_vector_field, param=search_params,
                                         limit=limit)
        # print("search cost", time.time() - start_time)

        # self.collection.release()
        return self.map_result_one_vector(list(results))

    @staticmethod
    def map_result_one_vector(results):
        list_results = []
        for k in range(len(results[0])):
            list_results.append({"id": results[0][k].id, "distance": results[0][k].distance})

        return list_results

    def query_by_face_id(self, list_face_id):
        expr = self.primary_name + " in " + str(list_face_id)
        # self.collection.load()
        output_fields = [self.primary_name, self.embedding_vector_field]
        res = self.collection.query(expr, output_fields)
        # self.collection.release()
        # print(res)
        return res



if __name__ == '__main__':
    milvus_staging_dal = CloverDAL(collection_name="clover_staging", partition_name="identities_hocsinh")
    milvus_staging_dal.create_collection()
    # milvus_staging_dal.collection.drop()