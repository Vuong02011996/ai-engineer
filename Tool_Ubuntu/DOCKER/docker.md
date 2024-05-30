# Docker
```
## Clear
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
## Install

### Set up docker repository
sudo apt-get update
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
### Install docker engine
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
```
# Docker compose
+ sudo apt  install docker-compose

# NVIDIA-Container-Toolkit (For run docker with gpu option)
+ [milvus_docker_gpu](https://milvus.io/docs/v1.0.0/milvus_docker-gpu.md)
+ https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker
