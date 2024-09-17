# Install
+ https://milvus.io/docs/install_standalone-docker-compose-gpu.md
+ `wget https://github.com/milvus-io/milvus/releases/download/v2.4.11/milvus-standalone-docker-compose-gpu.yml -O docker-compose.yml`
+ `sudo docker compose down`
+ `sudo rm -rf volumes`
+ Milvus with python: `pip install pymilvus==2.4.6`

# Milvus UI
+ https://github.com/zilliztech/attu
+ `docker run -p 40000:3000 -e MILVUS_URL=192.168.111.98:19530 zilliz/attu:v2.4`

# New features
+ Connect by `uri`
+ Get status collection by `get_load_state`
+ Create collection with id_type: s`tr = "int",  # or "string"`,
+ Create collection have 2 option create id: must field : `auto_id=True`
+ `get_collection_stats`: no return partition info(id_list, info partition, ...)
+ `describe_collection`: no full info : id list, ...
+ add field : `vector` when insert vector 
+ Have `upsert` to update data.
+ Have Dynamic Fields: json data, array, string, ...
+ Get entities from partitions must have ids 