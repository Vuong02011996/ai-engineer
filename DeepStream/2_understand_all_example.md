# deepstream-test1
+ a single H.264 stream: filesrc → decode → nvstreammux → nvinfer (primary detector) → nvdsosd → renderer.
# deepstream-test2
+ a single H.264 stream: filesrc → decode → nvstreammux → nvinfer (primary detector) → nvtracker → nvinfer (secondary classifier) → nvdsosd → renderer.
+  Use the various DeepStream SDK  elements in the pipeline and extract meaningful insights from a video stream
+ How to run:
  + cd /opt/nvidia/deepstream/deepstream-6.4/samples/streams
  + cp sample_qHD.h264 /opt/nvidia/deepstream/deepstream-6.4/sources/deepstream_python_apps/apps/deepstream-test2
  + cd /opt/nvidia/deepstream/deepstream-6.4/sources/deepstream_python_apps/apps/deepstream-test2
  + Run: `python3 deepstream_test_2.py sample_qHD.h264`

# deepstream-test3
+ Builds on deepstream-test1
+ Use multiple sources in the pipeline
+ accept any type of input (e.g. RTSP/File)
+ Configure Gst-nvstreammux to generate a batch of frames and infer on it for better resource utilization
+ Extract the stream metadata, which contains useful information about the frames in the batched buffer

+ Run 1 video: `python3 deepstream_test_3.py -i file:///opt/nvidia/deepstream/deepstream-7.0/samples/streams/sample_720p.mp4 `
+ Run 4 video:
  `python3 deepstream_test_3.py -i file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4`
+ Default using: 
    + MODEL: 
      + https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/blob/master/apps/deepstream-test3/deepstream_test_3.py#L331C10-L331C73
      + Using file config model: https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/blob/master/apps/deepstream-test3/dstest3_pgie_config.txt
      + samples/models/Primary_Detector/resnet18_trafficcamnet

# deepstream - detect face - deepstream-imagedata-multistream-redaction
+ https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/tree/master/apps/deepstream-imagedata-multistream-redaction
+ apt update
+ apt install python3-numpy python3-opencv -y


# Understand code 
## Example test 1
## Custom
+ In: /opt/nvidia/deepstream/deepstream-7.0/sources/deepstream_python_apps/apps/deepstream-test1
  + Run: python3 deepstream_test_1_custom_v1.py  sample_1080p_h264.mp4
+ cd /opt/nvidia/deepstream/deepstream-7.0/sources_python/apps/deepstream-test1
+ cp deepstream_test_1_custom_v1.py ../../../sources/deepstream_python_apps/apps/deepstream-test1