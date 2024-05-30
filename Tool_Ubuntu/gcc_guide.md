gcc --version
## Install gcc version 8
sudo apt -y install gcc-8 g++-8
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 8

## Select gcc version
 sudo update-alternatives --config gcc