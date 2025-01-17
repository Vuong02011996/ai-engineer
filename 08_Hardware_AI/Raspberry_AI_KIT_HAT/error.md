# Model beat
+ Step 1 Onnx - HAR: **Failed to determine type of layer to create in node**
    ```
    hailo_sdk_client.model_translator.exceptions.ParsingWithRecommendationException: Parsing failed. The errors found in the graph are:
     UnsupportedLSTMLayerError in op LSTM__159: activation types ['Sigmoid', 'Tanh', 'Tanh', 'Sigmoid', 'Tanh', 'Tanh'] are not supported
     UnsupportedSliceLayerError in op Slice__166: Failed to create slice layer at vertex Slice__166. Slice on axis 1 is not supported
     UnsupportedSliceLayerError in op Slice__171: Failed to create slice layer at vertex Slice__171. Slice on axis 1 is not supported
     UnsupportedShuffleLayerError in op stage_4/dense/Tensordot: Failed to determine type of layer to create in node stage_4/dense/Tensordot
     UnexpectedNodeError in op Squeeze__77: Unexpected node Squeeze__77 (Squeeze)
     UnexpectedNodeError in op Squeeze__98: Unexpected node Squeeze__98 (Squeeze)
     UnsupportedLSTMLayerError in op LSTM__182: activation types ['Sigmoid', 'Tanh', 'Tanh', 'Sigmoid', 'Tanh', 'Tanh'] are not supported
     UnsupportedSliceLayerError in op Slice__190: Failed to create slice layer at vertex Slice__190. Slice on axis 1 is not supported
     UnsupportedSliceLayerError in op Slice__196: Failed to create slice layer at vertex Slice__196. Slice on axis 1 is not supported
     UnexpectedNodeError in op Squeeze__119: Unexpected node Squeeze__119 (Squeeze)
     UnexpectedNodeError in op Squeeze__141: Unexpected node Squeeze__141 (Squeeze)
     UnsupportedShuffleLayerError in op stage_4/dense_1/Tensordot: Failed to determine type of layer to create in node stage_4/dense_1/Tensordot
    Please try to parse the model again, using these end node names: stage_4/bidirectional/forward_lstm/PartitionedCall/transpose, stage_4/tf.__operators__.getitem_3/strided_slice, Concat__153, stage_4/dense/Tensordot__804, stage_4/tf.__operators__.getitem_1/strided_slice, stage_4/dense/Tensordot/MatM
    ```
    + Fix : not yet

# Model Bi-LSTM
+  Optimize with dataset
  + Step2:  Optimize - quantization, with dataset 
    +     input_value = np.reshape(input_value, (1, len(input_value[1]),1))
          IndexError: list index out of range
    ```
      File "/home/server2/Downloads/hailo/lib/python3.10/site-packages/hailo_model_optimization/acceleras/hailo_layers/hailo_io.py", line 183, in validate_shape
      raise BadInputsShape(self.full_name, input_shape, data_shape)
      hailo_model_optimization.acceleras.utils.acceleras_exceptions.BadInputsShape: Data shape (5, 1) for layer bilstm_model/input_layer1 doesn't match network's input shape (1, 5, 1)
    ```
+  Optimize with dataset random
  + Step2: with CLI --use-random-calib-set data - OK 
  + Step3:

  ```
  Iteration #184 - Contexts: 5 
  [error] Mapping Failed (allocation time: 1m 44s)
  Compiler could not find a valid partition to contexts. Most commom error is: Automri finished with too many resources on context_2 with 62/184 failures.
  
  [error] Failed to produce compiled graph
  [error] BackendAllocatorException: Compilation failed: Compiler could not find a valid partition to contexts. Most commom error is: Automri finished with too many resources on context_2 with 62/184 failures.

  ```

# Model beat classified mexh
+ Step 2 without dataset `hailo optimize ../models/model_mexh.har --hw-arch hailo8l --use-random-calib-set`
    ```    
    File "/home/server2/Downloads/hailo/lib/python3.10/site-packages/hailo_model_optimization/acceleras/atomic_ops/concat_op.py", line 86, in <listcomp>
        shape.append(sum([input_shape[axis] for input_shape in input_shapes]))
    IndexError: tuple index out of range
   ```
