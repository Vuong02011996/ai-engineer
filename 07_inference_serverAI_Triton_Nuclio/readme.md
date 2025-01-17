# Request
+ deploy one model to server
+ Test inference

# Concepts
+ The inference server handles requests to process data, running the model, and returning results. 
+ **Nuclio**: Phù hợp cho các ứng dụng cần xử lý dữ liệu real-time, các tác vụ serverless tổng quát, và có thể triển khai mô hình máy học nhưng không chuyên biệt cho nhiệm vụ này
  + Hỗ trợ: Đa ngôn ngữ (Python, Node.js, Go, Ruby, Java, .NET Core, và nhiều ngôn ngữ khác).
+ **Triton Inference Server**: Phù hợp cho các ứng dụng cần triển khai mô hình máy học với hiệu suất cao và yêu cầu tối ưu hóa cho inference.
  + Hỗ trợ: Các framework máy học chính (TensorFlow, PyTorch, ONNX Runtime, XGBoost).

## Nuclio
+ How to setup nuclio server
+ What the input, output
+ Flow from input to output of nuclio server


+ Deep learning serverless functions: https://docs.cvat.ai/docs/manual/advanced/serverless-tutorial/
+ 

## Triton
+ https://developer.nvidia.com/blog/optimizing-and-serving-models-with-nvidia-tensorrt-and-nvidia-triton/
+ Convert from Tensorflow direct to TensorRT
  + https://docs.nvidia.com/deeplearning/frameworks/tf-trt-user-guide/index.html?ncid=partn-31097#supported-ops
  + https://blog.tensorflow.org/2021/01/leveraging-tensorflow-tensorrt-integration.html
  + Error: RuntimeError: Tensorflow has not been built with TensorRT support
+ AWS with triton server:
  + https://github.com/triton-inference-server/server/blob/main/deploy/aws/README.md