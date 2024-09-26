+ Clone submodule with file .gitmodules hoac clone each moudle
+ docker compose -f docker-compose.insightface.trt.yml

# Error
## external volume "mongodb_data_volume" not found
`docker volume create mongodb_data_volume`

## AttributeError: 'Minio' object has no attribute '_http'

## pymilvus 2.4.6 khong build duoc image
+ change to python version 3.8.19

# Build images face-recognition
+ docker build -t registry.oryza.vn/face-recognition-base:v1.1.0 .
+ docker tag registry.oryza.vn/face-recognition-base:v1.1.0 registry.oryza.vn/face-recognition-base:latest
+ 
# Git submodule
+ git submodule update --recursive
+ netstat -lntup
+ netstat -lntup|grep 900