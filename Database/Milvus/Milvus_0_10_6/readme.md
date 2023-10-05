# Build milvus 0.10.6 from image.
+ Pull Image from docker hub: [docker_hub](https://hub.docker.com/r/milvusdb/milvus/tags?page=1&ordering=last_updated)
+ docker pull milvusdb/milvus:0.10.6-gpu-d022221-64ddc2
+ create folder mongdb with 4 subfolder: db, conf, wal, logs.
+ Change some option in file server_config.yaml
  + Run GPU: 
    ```
    gpu:
    enable: true
    cache_size: 1GB
    gpu_search_threshold: 5
    ```
  ```
   gpu_search_threshold | A Milvus performance tuning parameter. This value will be  | Integer    | 1000            |
   #                      | compared with 'nq' to decide if the search computation will|            |                 |
   #                      | be executed on GPUs only.                                  |            |                 |
   #                      | If nq >= gpu_search_threshold, the search computation will |            |                 |
   #                      | be executed on GPUs only;                                  |            |                 |
   #                      | if nq < gpu_search_threshold, the search computation will  |            |                 |
   #                      | be executed on CPUs only.                                  |            |                 |
   #                      | The SQ8H index is special, if nq < gpu_search_threshold,   |            |                 |
   #                      | the search will be executed on both CPUs and GPUs.         |            |                 |
  ```
+ copy file server_config.yaml to conf.
  + conf of host
  + conf of container: sudo docker cp server_config.yaml 99d81b0b9853:/var/lib/milvus/conf (99d81b0b9853: container id)
+ change option in docker run in file install.sh -> and run bash install.sh.

## Install docker gpu

# Intall GUI milvus
+ [gui_milvus](https://zilliz.com/products/em)
+ docker pull milvusdb/milvus-em:v0.4.2
+ docker run --restart=always  -d -p 3033:80 milvusdb/milvus-em:v0.4.2
+ Run [localhost:3033](localhost:3033) Connect `192.168.111.133:8011`
