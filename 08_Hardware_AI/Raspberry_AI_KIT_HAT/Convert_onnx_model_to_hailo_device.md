# Hailo Dataflow Compiler Overview

+ Input: a trained Deep Learning model
+ Output: a binary file which is loaded to the Hailo device.
+ The `HailoRT API` is used for deploying the `built` model on the target device, used by the runtime applications.

## Model Build Process
  + several steps : `original model to a Hailo model -> model parameters optimization -> compilation.`
  + `HAR(Hailo representation format)` compressed file
    + HN files: HN model is a textual JSON output file 
    + NPZ files: weights as a NumPy NPZ file.

  + `Profiler tool - analyze Hailo model resources` uses the HAR file and profiles the expected performance of the model on hardware.
    + number of required devices
    + hardware resources utilization...
  + `Emulator`: allows users to run inference on their model without actual hardware. three main modes:
    + native mode: to validate the Tensorflow/ONNX translation process
    + fp_optimize mode : validate the model modifications
    + quantized mode: used to analyze the optimized model’s accuracy.
  + `Model Optimization`: After the user generates the HAR representation
    +  convert the parameters from float32 to integer representation.
    + The user should run the model emulation in native mode on a small set of images
    + generate a new network configuration for the integer representation (integer weights and biases, scaling configuration, and HW configuration.)
  + `Compiling the Model into a Binary Image`:
    + Now the model can be compiled into a HW compatible binary format with the extension HEF.
    + allocates hardware resources to reach the highest possible fps 
    + whole step is performed internally, `user’s perspective the compilation is done by calling a single API.`

## Dataflow Compiler Studio (Preview - Parsing stage only):
  + The Dataflow Compile Studio allows users to parse and visualize neural network graphs efficiently.
  + the GUI displays a side-by-side comparison of Hailo’s parsed graph and the original graph
  + https://hailo.ai/developer-zone/documentation/dataflow-compiler-v3-29-0/?sp_referrer=sdk%2Fcommand_line_tools.html%23using-dfc-studio

## Deployment Process
+ The HailoRT library provides access to the device in order to load and run the model.
+ This library is accessible from both C/C++ and Python APIs
+ A `Yocto layer` is provided to allow easy integration of HailoRT to embedded environments.

# Dataflow Compiler Installation
+ https://hailo.ai/developer-zone/documentation/dataflow-compiler-v3-29-0/?sp_referrer=install/install.html
+ Error:
  + ERROR: Could not build wheels for pygraphviz, which is required to install pyproject.toml-based projects
    + sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config
    + https://stackoverflow.com/questions/40266604/pip-install-pygraphviz-fails-failed-building-wheel-for-pygraphviz

# Dataflow Compiler Tutorials 
## Parsing Tutorial
+ Using CLI: `hailo parser {tf, onnx} --help.`
    ```
    Step1: Convert ONNX, TFLITE to HAR archie
    hailo parser tf beat-1.tflite --hw-arch hailo8l
  
    Step2: Optimize model Hailo HAR(Using 1024 sample data)
    hailo optimize beat-1.har --hw-arch hailo8l --use-random-calib-set
     
    Step3: Compiler model after Opimize to HEF
    
    hailo compiler --hw-arch hailo8l beat-1_optimized.har
     
    ```