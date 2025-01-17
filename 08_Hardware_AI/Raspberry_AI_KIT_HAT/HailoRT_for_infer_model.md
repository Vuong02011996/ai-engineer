# 
https://hailo.ai/developer-zone/documentation/hailort-v4-19-0/

# Install
## Available when install HAILO software
+ https://github.com/hailo-ai/hailo-rpi5-examples/blob/main/doc/install-raspberry-pi5.md#install-hailo-software
+ `sudo apt install hailo-all`
## Manual Install
+ https://hailo.ai/developer-zone/documentation/hailort-v4-19-0/?sp_referrer=install/install.html#installation-on-ubuntu

## Check Install on device 
+ In terminal (out or inside environment)
```
python3
from hailo_platform import HEF
```

# Inference
+ https://hailo.ai/developer-zone/documentation/hailort-v4-19-0/?sp_referrer=inference/inference.html
## HEF file
A HEF is Hailo’s binary format for neural networks. The HEF file contains:
+ Low level representation of the model
+ Target HW configuration
+ Weights
+ Metadata for HailoRT (e.g. input/output scaling)

## Inference with python
+ Python Async Inference Tutorial - Single Model
+ Python Async Inference Tutorial - Multiple Models
+ Python Inference Tutorial - Single Model
+ Python Inference Tutorial - Multi Process Service and Model Scheduler
+ Python Power Measurement Tutorial

# Monitor
+ https://hailo.ai/developer-zone/documentation/hailort-v4-20-0/?sp_referrer=cli/cli.html#monitor
+ `hailortcli monitor`