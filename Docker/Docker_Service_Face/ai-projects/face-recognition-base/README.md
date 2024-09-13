# Cài đặt môi trường
## Install GPU driver
    `sudo apt-get update
    sudo apt-get upgrade
    sudo ubuntu-drivers [select version driver]
    sudo reboot`

## Check version, install gcc, cuda, cudnn.
    `Ubuntu: lsb_release -a
    Cuda: nvcc -V
    Cudnn: ls /usr/local/cuda/lib64/libcudnn*
    gcc -v
    (We will need to install the gcc compiler as it will be used when installing the CUDA toolkit.)
            can ref: https://github.com/Vuong02011996/tools_ubuntu/blob/master/install.sh`

# Cài docker  

[docker](https://github.com/Vuong02011996/tools_ubuntu/blob/master/DOCKER/docker.md) - (Phải có trước docker gpu)

[ docker - gpu](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html.)
    
    Sau khi cài nvidia toolkit: sudo systemctl restart docker 
    Lỗi : Error response from daemon: could not select device driver "" with capabilities: [[gpu]]
    Check NVIDIA Container Toolkit đã được cài đặt trên ubuntu
    dpkg -l | grep nvidia-container-toolkit

`sudo apt install docker-compose : docker compose`

# Cài Database
## MongoDB
    https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
    Cài đặt mongo compass, view data.

## MilvusDB
    https://milvus.io/docs/v2.1.x/install_standalone-aptyum.md
    Cài milvus gui, xem data.
    Firebase.

# Chạy model face detection and face recognition on docker.
    Clone : git clone https://github.com/SthPhoenix/InsightFace-REST.git
    Run file deploy_trt.sh

## Setup và chạy project nhận diện khuôn mặt
    Pycharm
    Cài anaconda
    https://docs.anaconda.com/free/anaconda/install/linux/
    Download project - zip or git
    Tạo môi trường conda 
    install requirements.txt

# Chạy chương trình test video hoặc camera.
    Copy .env_copy ->.env
    Run server.py

# Code:
    align_face: https://github.com/Vuong02011996/Clover/blob/vuong_dev/app/app_utils/face_local_utils.py#L54

# Delete logs milvus
+ 