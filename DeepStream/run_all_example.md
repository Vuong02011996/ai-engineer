# deepstream-test1
+ a single H.264 stream: filesrc → decode → nvstreammux → nvinfer (primary detector) → nvdsosd → renderer.
# deepstream-test2
+ a single H.264 stream: filesrc → decode → nvstreammux → nvinfer (primary detector) → nvtracker → nvinfer (secondary classifier) → nvdsosd → renderer.
+ Add (secondary classifier)
# deepstream-test3
+ Builds on deepstream-test1
+ Use multiple sources in the pipeline
+ accept any type of input (e.g. RTSP/File)
+ Configure Gst-nvstreammux to generate a batch of frames and infer on it for better resource utilization
+ Extract the stream metadata, which contains useful information about the frames in the batched buffer

python3 deepstream_test_3.py -i file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 
Run 4 video:
python3 deepstream_test_3.py -i file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4 file:///opt/nvidia/deepstream/deepstream-6.4/samples/streams/sample_720p.mp4

# deepstream - detect face - deepstream-imagedata-multistream-redaction
+ https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/tree/master/apps/deepstream-imagedata-multistream-redaction
+ apt update
+ apt install python3-numpy python3-opencv -y
+ 