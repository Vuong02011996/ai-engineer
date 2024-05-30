+ https://docs.nvidia.com/metropolis/deepstream/dev-guide/index.html

# Ref
+ https://hackmd.io/@congphu/SkN6RIXY_
# NGC 
+ Nvidia GPU cloud (NGC) is a GPU-accelerated cloud platform optimized for deep learning and scientific computing.
# Nvidia
+ All documents : https://docs.nvidia.com/#all-documents
+ All SDK-Nvidia(157): https://developer.nvidia.com/sdk-glossary
  + **Computer Vision/Video Analytics**: 
    + **DeepStream**
    + **TAO Toolkit**: NVIDIA Train, Adapt, and Optimize (TAO) Toolkit gives you a faster, easier way to accelerate training and quickly create highly accurate and performant, domain-specific AI models.
    + **TensorRT**: NVIDIA® TensorRT™ is an SDK for high-performance deep learning inference. It includes a deep learning inference optimizer and runtime that delivers low latency and high throughput for deep learning inference applications
    + **TensorRT - ONNX Runtime**
    + **Triton Inference Server**:NVIDIA Triton™ Inference Server delivers fast and scalable AI in production. Triton Inference Server streamlines AI inference by enabling teams to deploy, run and scale trained AI models from any framework on any GPU- or CPU-based infrastructure.
  
  + **Video Streaming/Conferencing**:
    + **Video Codec SDK**: 
    + **NGC AI Models**: State-of-the-art AI models from NVIDIA NGC help data scientists and developers quickly build custom models or use them as is for inference.
  ....
# DeepStream SDK
+ https://developer.nvidia.com/deepstream-getting-started
+ All documents: https://docs.nvidia.com/metropolis/deepstream/dev-guide/
+ Error and forums: https://forums.developer.nvidia.com/c/accelerated-computing/intelligent-video-analytics/deepstream-sdk/15

+ DeepStream Python Apps: https://github.com/NVIDIA-AI-IOT/deepstream_python_apps
  + Only supports Ubuntu 22.04 for DeepStreamSDK 6.4 with Python 3.10 and gst-python 1.20.3
  + DeepStream_Python_Apps_Bindings_v1.1.8: Ubuntu 20.04, python 3.8, DeepStream sdk 6.3
  + Version deep stream python:  https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/releases

+ DeepStream with Dockers: 
  + https://github.com/NVIDIA-AI-IOT/deepstream_dockers

# Install deepstream 
+ https://gist.github.com/bharath5673/800a18cc7474ce9c22fda6deaaa98354
+ https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_Quickstart.html
+ With docker:
  + https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_docker_containers.html
  + https://github.com/NVIDIA-AI-IOT/deepstream_dockers
  + 
## DeepStream with FaceDetection
### Paper 
+ https://www.researchgate.net/publication/363174783_Robust_Multi-Sensor_Facial_Recognition_in_Real_Time_using_Nvidia_DeepStream
  + 
### Github ref 
+ Note :
  + Using make to run app -> install without docker
  

+ https://github.com/hiennguyen9874/deepstream-face-recognition - 15*VN - Xuan Hien
  + Test on dGPU
  + Face detection model: yolov7-face -> onnx -> tensorRT
  + Face recognition: webface_r50.onnx from deepinsight -> tensorRT
  + Usage: with docker and without docker 
  + sudo docker run --gpus all  --rm -it -v $(pwd):/app hiennguyen9874/deepstream-face-recognition:deepstream-6.0.1 Error:
    + bash: ./bin/deepstream-app: No such file or directory

+ https://github.com/zhouyuchong/face-recognition-deepstream/tree/main - zhouyuchong - 47*
  + Deepstream app use retinaface and arcface for face recognition.
  + The same author: https://github.com/zhouyuchong/retinaface-deepstream-python - face detection.
  + retinaface + arcface 
  + Using Kafka service 
  + Usage : docker 

+ https://github.com/marcoslucianops/DeepStream-Yolo-Face  - marcoslucianops - 47*
  + NVIDIA DeepStream SDK 6.3 / 6.2 / 6.1.1 / 6.1 / 6.0.1 / 6.0 application for YOLO-Face models
  + 7 months ago 
  + Video demo : https://www.youtube.com/MarcosLucianoTV
  + No using docker


+ https://github.com/NNDam/deepstream-face-recognition - NNDam - 6* 
  + Face detection -> alignment -> feature extraction with deepstream
  + Using docker file to build service

+ https://github.com/nghiapq77/face-recognition-deepstream - nghiapq77 - 36* 
  + This is a face recognition app built on DeepStream reference app.
  + RetinaFace and ArcFace is used for detection and recognition respective
  + 3 years ago - DeepStream 5.0 
  + No using docker .


+ https://github.com/edu-417/deepstream-face-recognition/tree/main - edu-417 0* 
  + This project uses nvidia deepstream to make an real time video face recognition app
  + Không có hướng dẫn rõ ràng nhưng sử dụng docker và deepstream mới nhất .

+ https://github.com/Kojk-AI/deepstream-face-recognition - Kojk-AI - 3*
  + Sample face-recognition app using Deepstream 6.0.1 with FaceNet on **Jetson Nano** (L4T Jetpack 4.6.1)

+ https://github.com/riotu-lab/deepstream-facenet/tree/master - riotu-lab - 42 *
  + 3,4  years ago 
  + Face Recognition on **Jetson Nano** using DeepStream and Python.
  + No using docker 

  

  
