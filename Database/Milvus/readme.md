# Install Milvus server
+ [install_standalone-docker](https://milvus.io/docs/v2.0.0/install_standalone-docker.md)

# Milvus client(python)
+ ```pip install pymilvus-orm==2.0.0rc4```

# Milvus Insight(GUI)
+ [insight_install](https://milvus.io/docs/v2.0.0/insight_install.md)
+ ```commandline
    docker run -p 8000:3000 -e HOST_URL=http://{ your machine IP }:8000 -e MILVUS_URL={your machine IP}:19530 milvusdb/milvus-insight:latest
    docker run --restart=always -p 3003:3000 -e HOST_URL=http://0.0.0.0:3003 -e MILVUS_URL=0.0.0.0:19530 milvusdb/milvus-insight:latest
    ```
+ http://0.0.0.0:3003 -> connect 192.168.1.8:19530

# How to use
**1. Connect**
```python
from pymilvus_orm import connections
connections.connect("default", host='localhost', port='19530')
```
**2. Create**
   1. Create collection
      1. The created collection must contain *a primary key field*
      2. Prepare collection parameters:
         1. Collection name
         2. Field parameters.
      3. Call _Collection()_ provided by the Milvus instance to create a collection.
      4. Example:
         ```python
         from pymilvus_orm import Collection, CollectionSchema, FieldSchema, DataType
         
         pk = FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True)
         
         collection_name = "example_collection"
         field_name = "example_field"
         field = FieldSchema(name=field_name, dtype=DataType.FLOAT_VECTOR, dim=8)
         schema = CollectionSchema(fields=[pk,field], description="example collection")
         
         collection = Collection(name=collection_name, schema=schema)
         
         # Get an existing collection by its name.
         collection = Collection(name=collection_name)
         
         # Check if the collection is created successfully
         pymilvus_orm.utility.get_connection().has_collection(collection_name)
         True
         
         # List all created collections
         pymilvus_orm.utility.get_connection().list_collections()
         ['example_collection']
         
         # View collection statistics, such as row count
         collection.num_entities
         0
         ```
   2. Create a partition
      1. To improve search efficiency, divide a collection into several partitions by name
      2. Milvus creates a default partition name, **_default**, for new collections
      3. Example
      ```python
      partition_name = "example_partition"
      partition = collection.create_partition(partition_name)   
      
      # Check
      collection.partitions
      [{"name": "_default", "description": "", "num_entities": 0}, {"name": "example_partition", "description": "", "num_entities": 0}]
      
      # Call has_partition() to check if a partition is successfully created.
      collection.has_partition(partition_name)
      ```

**3. Insert**
1. You can insert vectors to a specified partition within a specific collection
2. Insert the random vectors to the newly created collection. Milvus automatically assigns IDs to the inserted vectors
3. Milvus returns the value of MutationResult(mr), which contains the corresponding primary_keys of the inserted vectors
4. By specifying partition_name when calling insert()
5. Milvus temporarily stores the inserted vectors in the memory. Call flush() to flush them to the disk
6. Example
```python
# Generate random vectors
import random
vectors = [[random.random() for _ in range(8)] for _ in range(10)]
entities = [vectors]

mr = collection.insert(entities)

# check
mr.primary_keys
[425790736918318406, 425790736918318407, 425790736918318408, ...]

# insert specifying partition
collection.insert(data=entities, partition_name=partition_name)

# Flush them to the disk
pymilvus_orm.utility.get_connection().flush([collection_name])
```

**4. Delete** 
1. Drop a partition
2. Drop a collection
3. Delete entities: This feature is still under development and will be available when a stable version of Milvus 2.0 is released
4. Example
```python
collection.drop_partition(partition_name=partition_name)
collection.drop()
```
**5. Build an Index**
1. Create an index for a specified field in a collection to accelerate vector similarity search
2. Example
```python
# Prepare the index parameters
index_param = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":1024}
    }

# Build an Index
collection.create_index(field_name=field_name, index_params=index_param)

# View Index details
collection.index().params
{'metric_type': 'L2', 'index_type': 'IVF_FLAT', 'params': {'nlist': 1024}}
```

**6. Search and query**
1. Conduct a vector similarity search
   1. Create search parameters
   2. Load the collection to memory before conducting a vector similarity search
   3. Call search() with the newly created random vectors query_records
   4. Milvus returns the IDs of the most similar vectors and their distances.
   5. To search in a specific partition or field, set the parameters partition_names and fields when calling search()
   6. Release the collections loaded in Milvus to reduce memory consumption when the search is completed
   7. Example:
   ```python
   search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
   collection.load()
   results = collection.search(vectors[:5], field_name, param=search_params, limit=10, expr=None)
   
   # check
   results[0].ids
   [424363819726212428, 424363819726212436, ...]
   results[0].distances
   [0.0, 1.0862197875976562, 1.1029295921325684, ...]
   
   collection.search(vectors[:5], field_name, param=search_params, limit=10, expr=None, partition_names=[partition_name])
   collection.release()
   ```
   
2. Conduct a Hybrid Search(search kết hợp)
3. Query


# Note
+ entities ~ document.

# Reference
[milvus.io](https://milvus.io/docs/v2.0.0/home)