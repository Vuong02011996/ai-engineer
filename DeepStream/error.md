1. python3 deepstream_test_1.py sample_1080p_h264.mp4 
   + Creating Source : waiting > 10s ...(hang forever…)
   + https://forums.developer.nvidia.com/t/deepstream-6-4-problem-with-gst-registry-cache/277830
   + ls ~/.cache/gstreamer-1.0/registry.x86_64.bin
   + rm ~/.cache/gstreamer-1.0/registry.x86_64.bin
2. No protocol specified
    +  export DISPLAY=:0 ,  export DISPLAY=:1 
    + before you run docker, first run xhost +
   
3. GLib (gthread-posix.c): Unexpected error from C library during 'pthread_setspecific': Invalid argument.  Aborting.
   + rm ~/.cache/gstreamer-1.0/registry.x86_64.bin
4. ERROR from primary_gie: gstnvinferserver_impl start failed 
   + when plugin-type = 1 to use nvinferserver 
   + Triton Server Settings 
   + Maintain
5. ImportError: libavcodec.so.58: cannot open shared object file: No such file or directory
   + Error when run example deepstream-imagedata-multistream-redaction have import cv2
   + 