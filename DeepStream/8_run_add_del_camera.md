# Run example 
```
+ `export DISPLAY=:1`
+ `xhost +`
+ ```sudo docker start d2```: start docker d2
+ ```sudo docker exec -it d2 bash```: go to contain and run example again.

cd : /opt/nvidia/deepstream/deepstream-6.4/sources/deepstream_python_apps/apps/runtime_source_add_delete
rm ~/.cache/gstreamer-1.0/registry.x86_64.bin
RUN: 
python3 deepstream_rt_src_add_del.py \
  file:///opt/nvidia/deepstream/deepstream/samples/streams/sample_720p.mp4
```

# Understand code 

# Using deepstream-7.0
+ https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_plugin_gst-nvmultiurisrcbin.html#introduction
+ how **nvmultiurisrcbin** integrates: `nvds_rest_server(REST API Server) + nvurisrcbin + nvstreammux`
  + REST API Server; nvds_rest_server: `/opt/nvidia/deepstream/deepstream/sources/libs/nvds_rest_server/`
  + nvmultiurisrcbin: `/opt/nvidia/deepstream/deepstream/sources/gst-plugins/gst-nvmultiurisrcbin/`
  + deepstream-test5-app Demonstrating usage of nvmultiurisrcbin with nvmsgconv and nvmsgbroker: `/opt/nvidia/deepstream/deepstream/sources/apps/sample_apps/deepstream-test5/`

+ Run:
```commandline
  gst-launch-1.0 nvmultiurisrcbin \
  port=9000 ip-address=localhost \
  batched-push-timeout=33333 max-batch-size=10 \
  drop-pipeline-eos=1 live-source=1 \
  uri-list=file:///opt/nvidia/deepstream/deepstream/samples/streams/sample_1080p_h264.mp4,file:///opt/nvidia/deepstream/deepstream/samples/streams/sample_1080p_h264.mp4 width=1920 height=1080 \
  ! nvmultistreamtiler ! nveglglessink
```