1. OSError: libcublas.so.10: cannot open shared object file: No such file or directory

```conda install -c anaconda cudatoolkit=10.1```

2. Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory in tensorflow
   + Check tensorflow match with cuda version.[here](https://www.tensorflow.org/install/source#gpu)
   
3. How can i solve InvalidArgumentError: cycle_length must be > 0 when load tfrecords file
   + ref [here](https://stackoverflow.com/questions/59775373/how-can-i-solve-invalidargumenterror-cycle-length-must-be-0-when-load-tfrecor)
   + i encountered similar problem, on tensorflow 2.0, however,upgrading to 2.1 solves the issue

3. Process finished with exit code 137 (interrupted by signal 9: SIGKILL) out of RAM 
   + => GPU not activate.

4. Could not load dynamic library 'libcublas.so.10'; dlerror: libcublas.so.10: cannot open shared object file: No such file or directory
   + conda install -c anaconda cudatoolkit=10.1
   
5. OSError: libnccl.so.2: cannot open shared object file: No such file or directory
   + ref in [here](https://stackoverflow.com/questions/66786887/getting-oserror-libnccl-so-2-while-importing-mxnet)
   + downgraded to mxnet-cu101==1.7 

5. Could not load dynamic library 'libcudnn.so.7'; dlerror: libcudnn.so.7: cannot open shared object file: No such file or directory
   + sudo ldconfig /usr/local/cuda/lib64

## TensorRT

1. Error in verifyHeader: 0 (Version tag does not match. Note: Current Version: 96, Serialized Engine Version: 87)
    
    ```If the engine was created and ran on different versions```

## Tensorflow 1.0 to 2.0

1. ModuleNotFoundError: No module named 'tensorflow.contrib' import slim
   https://github.com/google-research/tf-slim
   import tf_slim as slim
   
2. AttributeError: module 'tensorflow' has no attribute 'GraphKeys'
   import tensorflow as tf -> import tensorflow.compat.v1 as tf
   
3. RuntimeError: tf.placeholder() is not compatible with eager execution.
   tf.compat.v1.disable_eager_execution()
   
4. attributeerror 'int' object has no attribute 'value'
   variable_parameters *= dim.value -> variable_parameters *= dim