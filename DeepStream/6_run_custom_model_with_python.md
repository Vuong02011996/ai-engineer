# Run in nvinfer 
## Inference Available model in deepstream
+ File config all : application -> tiled-display -> source0 -> streammux -> sink0 -> osd -> primary-gie -> sink1 -> sink2 -> tracker
  + /opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models/deepstream_app_source1_peoplenet.txt
+ File config model(primary-gie):
  + https://github.com/NVIDIA-AI-IOT/deepstream_reference_apps/blob/master/deepstream_app_tao_configs/nvinfer/config_infer_primary_peoplenet.txt

## Custom with TAO models
+ https://github.com/NVIDIA-AI-IOT/deepstream_tao_apps?tab=readme-ov-file#information-for-customization
+ run tao-export to generate an **.etlt** model
+ **.etlt** model can be deployed into DeepStream for fast inference as this sample shows.
+ You can also convert the etlt model to TensorRT engine file using tao-converter
+ The _TensorRT engine file is hardware dependent_, while the .etlt model is not.

## Custom test3 with tao models peopleNet 
+ https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/blob/master/apps/deepstream-test3/README
+ cd /opt/nvidia/deepstream/deepstream-6.4/sources/deepstream_python_apps/apps/deepstream-test3
+ run :` python3 deepstream_test_3.py -i file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 --pgie nvinfer -c config_infer_primary_peoplenet.txt`
  + if --pgie is not specified, test3 uses nvinfer and default model, not peoplenet.
  + Both --pgie and -c need to be provided for custom models.
+ labels: 
  + cd /opt/nvidia/deepstream/deepstream/samples/configs/tao_pretrained_models
  + cat labels_peoplenet.txt `Person Bag Face`
+ Run with rtsp: Unauthorized
  `python3 deepstream_test_3.py -i rtsp://admin:oryza@2023@192.168.111.63:7001/9a5dcef8-8028-5c36-56b9-ee51381f454d --pgie nvinfer -c config_infer_primary_peoplenet.txt`

## custom model retinaface and arcface
