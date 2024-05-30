# Choice docker image
+ https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_docker_containers.html
+ docker pull nvcr.io/nvidia/deepstream:6.4-gc-triton-devel: all for development 
+ docker pull nvcr.io/nvidia/deepstream:6.4-triton-multiarch: for development but not graph composer
+ docker pull nvcr.io/nvidia/deepstream:6.4-samples-multiarch: contains the runtime libraries - not for development.

# Run docker 
+ ```export DISPLAY=:0```: :0 typically represents the first display server, which is the default for most systems.
+ ```xhost +```: This command grants permission to all hosts to connect to the X server. + here means allowing all hosts to connect to the X server.
+ ```sudo docker run -it --rm --net=host --gpus all -e DISPLAY=$DISPLAY --device /dev/snd -v /tmp/.X11-unix/:/tmp/.X11-unix b8```
  + -it: interactive terminal via the command line.
  + --rm: Automatically removes the container when it exits.
  + --net=host: enabling access to network services available on the host directly.
  + --gpus all: all GPUs available on the host should be made accessible to the container
  + -e DISPLAY=$DISPLAY: enabling GUI applications within the container to connect to the host's X server for display.
  + --device /dev/snd: Mounts the host's sound device (/dev/snd) into the container, allowing audio input/output within the container
  + -v /tmp/.X11-unix/:/tmp/.X11-unix:  Mounts the host's X11 Unix socket (/tmp/.X11-unix/) into the container, 
    facilitating communication between GUI applications within the container and the host's X server for display.
  + b8: image id 
# Go into the container again
+ Before start container to avoid error `No protocol specified` run:
  + `export DISPLAY=:1`
  + `xhost +`
+ ```sudo docker start d2```: start docker d2
+ ```sudo docker exec -it d2 bash```: go to contain and run example again.

# Run example python 
+ Get into container : docker run -it or docker exec -it 
+ cd to : /opt/nvidia/deepstream/deepstream-6.4/sources
+ git clone https://github.com/NVIDIA-AI-IOT/deepstream_python_apps
## Build bindings
+ https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/tree/master/bindings
### 1 Prerequisites
  + download and install Deepstream SDK (Step pull and Run docker )
 
  + Base dependencies : IN /opt/nvidia/deepstream/deepstream-6.4
    + apt-get update 
    + ``` 
      apt install python3-gi python3-dev python3-gst-1.0 python-gi-dev git meson \
      python3 python3-pip python3.10-dev cmake g++ build-essential libglib2.0-dev \
      libglib2.0-dev-bin libgstreamer1.0-dev libtool m4 autoconf automake libgirepository1.0-dev libcairo2-dev
      ```
    + Initialization of submodules
      + cd /opt/nvidia/deepstream/deepstream/sources/deepstream_python_apps/ 
      + git submodule update --init : utilizes gst-python and pybind11 submodules
    + Installing Gst-python
      + apt-get install -y apt-transport-https ca-certificates -y
      + update-ca-certificates
      
    ```commandline
    cd 3rdparty/gstreamer/subprojects/gst-python/
    meson build
    meson configure
    cd build
    ninja
    ninja install
    ```
### 2 Compiling the bindings
    ```commandline
    cd deepstream_python_apps/bindings
    mkdir build
    cd build
    cmake ..
    make -j$(nproc)
    ```

### 3 Installing the bindings
    ```commandline
    pip3 install ./pyds-1.1.10-py3-none*.whl
    ```
### Run example 
+ cd /opt/nvidia/deepstream/deepstream-6.4/samples/streams
+ cp sample_1080p_h264.mp4 /opt/nvidia/deepstream/deepstream-6.4/sources/deepstream_python_apps/apps/deepstream-test1
+ cd sources/deepstream_python_apps/apps/deepstream-test1
+ run : python3 deepstream_test_1.py sample_1080p_h264.mp4 
+ `python3 deepstream_test_1.py file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_1080p_h264.mp4`


