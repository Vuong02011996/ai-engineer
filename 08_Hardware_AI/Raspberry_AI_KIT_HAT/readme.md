# Hailo 
+ Hailo - nhà sản xuất bộ vi xử lý tích hợp trí tuệ nhân tạo, được thành lập tại Israel vào năm 2017, 
+ Hailo đã phát triển các bộ vi xử lý AI hoạt động tốt nhất thế giới cho các lĩnh vực khác nhau như ngành sản xuất ô tô,
hệ thống giao thông thông minh, công nghệ 4.0, bán lẻ thông minh, camera thông minh,..

# Hardware
+ 3 TYPE:
  + Generative AI Accelerators: Hailo-10H - Generative AI Acceleration Module(LLM)
  + AI Vision Processors: Hailo 15 - Hailo-15 AI Vision Processor - computer Vision
  + AI Accelerators: Hailo 8, 8L, 8R
## AI Accelerators vs Raspberry Pi 5
  + Run command to check type of Hailo: `hailortcli fw-control identify` => **Device Architecture: HAILO8L**
  + Hailo-8L (13 TOPS) - Hailo-8L has half the amount of compute elements(compare Hailo 8), the rest is identical.
  + Hailo-8 (26 TOPS 	Tera-Operations Per	Second).
  + More info about Hardware: https://hailo.ai/products/ai-accelerators/hailo-8l-m-2-ai-acceleration-module-for-ai-light-applications/#hailo8lm2-overview

+ **M.2 HAT (Hardware Attached on Top)**
  + M.2 HAT: Là một bo mạch mở rộng được thiết kế để kết nối với Raspberry Pi thông qua giao diện M.2. 
  + Nó cho phép gắn các mô-đun như Hailo-8 vào Raspberry Pi, cung cấp khả năng tăng tốc tính toán AI một cách dễ dàng.

# DFC - Dataflow Compiler Installation

+ https://hailo.ai/products/hailo-software/hailo-ai-software-suite/#sw-dc - DFC Architecture


  + Download DFC tool: https://hailo.ai/developer-zone/software-downloads/ 
  + Read guide to convert model using DFC: https://hailo.ai/developer-zone/documentation/dataflow-compiler-v3-29-0/?sp_referrer=install/install.html
  + 
+ Dataflow Compiler (DFC) Availability!
  + https://community.hailo.ai/t/dataflow-compiler-dfc-availability/1476
  + BYOD:(Bring Your Own Data) allows you to fine-tune or retrain existing models from the Hailo Model Zoo, such as YOLO or ResNet, using your custom datasets to adapt them for specific applications. 
  + BYOM:(Bring Your Own Model) enables you to bring your pre-trained or custom-designed models (e.g., TensorFlow, PyTorch, or ONNX) and deploy them on Hailo’s hardware, like the Hailo-8 or Hailo-15, using the Hailo toolchain.

+ **Note:** Use `hw_arch=hailo8l` to compile for Hailo-8L device, such as: Hailo-8L, or custom Chip-on-Board solutions.

# Onnxruntime vs Hailo
+ https://github.com/hailo-ai/onnxruntime/blob/hailo/hailo/README.md
  + Convert your ONNX model with DFC tool.
  + Create the ONNXRuntime session with "HailoExecutionProvider" in the execution providers list, and run the ONNX model

# HailoRT - Document
+ https://hailo.ai/developer-zone/documentation/hailort-v4-19-0/


# RPI 5 vs Hailo
+ https://github.com/hailo-ai/hailo-rpi5-examples

# Hailo and available model 
+ https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/HAILO_MODELS.rst

# TAPPAS - full application examples - don't care this time
+ Optimized Execution of **Video**-Processing Pipelines
+ TAPPAS is Hailo's set of full application examples, implementing pipeline elements and pre-trained AI tasks.