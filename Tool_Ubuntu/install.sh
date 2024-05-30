#!/bin/bash

# Install GPU drivers.
#sudo ubuntu-drivers autoinstall
#sudo reboot

# Install cuda 10.01
# link https://medium0.com/@stephengregory_69986/installing-cuda-10-1-on-ubuntu-20-04-e562a5e724a0
# Clean up
#sudo rm /etc/apt/sources.list.d/cuda* -y
#sudo apt remove --autoremove nvidia-cuda-toolkit -y
#sudo apt remove --autoremove nvidia-* -y
#
#sudo apt-get purge nvidia* -y
#sudo apt-get autoremove -y
#sudo apt-get autoclean -y
#
#sudo rm -rf /usr/local/cuda*
#
#### Install cuda 10.1
#sudo apt update
#sudo add-apt-repository ppa:graphics-drivers -y
#sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
#sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
#sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda_learn.list'
#sudo apt update
#sudo apt install cuda-10-1 -y

### Install cuda 11.0.2
#wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
#sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
#wget http://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda-repo-ubuntu2004-11-0-local_11.0.2-450.51.05-1_amd64.deb
#sudo apt install ./cuda-repo-ubuntu2004-11-0-local_11.0.2-450.51.05-1_amd64.deb
#sudo apt-key add /var/cuda-repo-ubuntu2004-11-0-local/7fa2af80.pub
#sudo apt-get update
#sudo apt-get -y install cuda
#
### Add PATH
#echo 'export PATH=/usr/local/cuda-10.1/bin${PATH:+:${PATH}}' >> ~/.bashrc
#echo 'export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
#source ~/.bashrc
#sudo ldconfig
#sudo apt install libcudnn7

# Go to link https://developer.nvidia.com/rdp/cudnn-archive, click the following: “Download cuDNN v7.5.0 (Feb 21, 2019), for CUDA 10.0” and then “cuDNN Library for Linux” and install:

# tar -xf cudnn-10.0-linux-x64-v7.5.0.56.tgz
# sudo cp -R cuda/include/* /usr/local/cuda-10.1/include
# sudo cp -R cuda/lib64/* /usr/local/cuda-10.1/lib64


# Install Anaconda

#rm -rf ~/anaconda3 ~/.condarc ~/.conda ~/.continuum
#sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 -y
#wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
#sha256sum /tmp/Anaconda3-2020.02-Linux-x86_64.sh
#bash /tmp/Anaconda3-2020.02-Linux-x86_64.sh -y
#source /home/$USER/.bashrc
#conda config --set auto_activate_base false

# Install rapids conda envs
# https://rapids.ai/start.html
#conda create -n rapids-0.18 -c rapidsai -c nvidia -c conda-forge \
#    -c defaults rapids-blazing=0.18 python=3.7 cudatoolkit=10.1


# Docker
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
# docker compose
sudo apt  install docker-compose
#### Verify
#sudo docker run hello-world



# Install Pycharm
# sudo snap install pycharm-community --classic

# Remmina
# sudo snap install remmina

# Với ubuntu 20.04 mặc định là cuda 10.1
Cài gpu driver: sudo install nvidia-driver-535
Cài cuda 10.1: sudo apt -y install nvidia-cuda-toolkit
https://www.server-world.info/en/note?os=Ubuntu_20.04&p=cuda&f=1
