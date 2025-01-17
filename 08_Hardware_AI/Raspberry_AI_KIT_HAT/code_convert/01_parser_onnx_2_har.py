# General imports used throughout the tutorial
import tensorflow as tf
from IPython.display import SVG

# import the ClientRunner class from the hailo_sdk_client package
from hailo_sdk_client import ClientRunner

chosen_hw_arch = "hailo8l"
# For Hailo-15 devices, use 'hailo15h'
# For Mini PCIe modules or Hailo-8R devices, use 'hailo8r'

onnx_model_name = "model_mexh"
onnx_path = f"../models/{onnx_model_name}.onnx"

runner = ClientRunner(hw_arch=chosen_hw_arch)
hn, npz = runner.translate_onnx_model(
    onnx_path,
    onnx_model_name,
    # start_node_names=["input.1"],
    # end_node_names=[],
    # net_input_shapes={"input.1": [1, 1, 100, 100]},
    net_input_shapes={"input.1": [1, 1, 100, 100]},
)

hailo_model_har_name = "../models/" + f"{onnx_model_name}.har"
runner.save_har(hailo_model_har_name)

"""
Visualize the graph with Hailo’s visualizer tool:
!hailo visualizer {hailo_model_har_name} --no-browser
SVG("resnet_v1_18.svg")
hailo visualizer ../models/lstm_model.har
"""
