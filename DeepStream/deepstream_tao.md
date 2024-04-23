
peoplenet model -> 
/opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models/README.md
-> https://github.com/NVIDIA-AI-IOT/deepstream_reference_apps.git
-> deepstream_reference_apps/deepstream_app_tao_configs/
-> https://github.com/NVIDIA-AI-IOT/deepstream_tao_apps


# deepstream_tao_apps
Integrate TAO model with DeepStream SDK
+ https://github.com/NVIDIA-AI-IOT/deepstream_tao_apps
Sample apps to demonstrate how to deploy models trained with TAO on DeepStream

# deepstream_reference_apps
This repository contains the reference applications for video analytics tasks using TensorRT and DeepSTream SDK 6.4.
+ https://github.com/NVIDIA-AI-IOT/deepstream_reference_apps/tree/master
+ Have three different reference applications: pps-common, audio_apps, **sample_apps**
+ Have 5 app/project to reference:
  + back-to-back-detectors: The project shows usage of 2 detectors in cascaded mode
  + deepstream-bodypose-3d: The project demonstrates usage of Body Pose 3D model in Deepstream application
  + **deepstream_app_tao_configs**: 
  + **runtime_source_add_delete**:The project demonstrates addition and deletion of video sources in a live Deepstream pipeline.
## deepstream_app_tao_configs
https://github.com/NVIDIA-AI-IOT/deepstream_reference_apps/tree/master/deepstream_app_tao_configs
### Guide to download pre-trained TAO models 
/opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models/README.md
+ Downloading the config files and model download script
  + Config files and Models download script are now present in
  https://github.com/NVIDIA-AI-IOT/deepstream_reference_apps under `deepstream_app_tao_configs`
  + Results: file download_models.sh int /opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models/
+ Downloading the models
  + cd /opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models/
  + ./download_models.sh
  + List model: 
    + Detection Network: Faster-RCNN / YoloV3 / YoloV4 /SSD / DSSD / RetinaNet/ UNET/
    + Classification Network: 
    + Other Networks: PeopleNet, FaceDetectIR, dashcamnet / vehiclemakenet / vehicletypenet
 / trafficcamnet / facedetectir / facenet
+ Models saved : /opt/nvidia/deepstream/deepstream/samples/models/tao_pretrained_models
  + Face - person: facedetectir, facenet, peopleNet, peopleSegNet, retinanet

### Guide to  run pre-trained TAO models 
+ After download cd /opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models
+ Run: deepstream-app -c deepstream_app_source1_peoplenet.txt
+ Change: 
  + #(0): nvinfer; (1): nvinferserver
  + plugin-type=1 => Error 


### Triton Server Settings
