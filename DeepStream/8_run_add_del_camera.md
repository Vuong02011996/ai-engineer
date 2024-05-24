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
+ 