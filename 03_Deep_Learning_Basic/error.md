# TF1 - TF2
+ Only using this code:
```
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()
  ```
+ AttributeError: module 'tensorflow' has no attribute 'Session'. Did you mean: 'version'?
  + To get TF 1.x like behaviour in TF 2.0 one can run: `tf.compat.v1.Session() instead of tf.Session()`
  + https://stackoverflow.com/questions/55142951/tensorflow-2-0-attributeerror-module-tensorflow-has-no-attribute-session
  
+ ‘RuntimeError: The Session graph is empty. Add operations to the graph before calling run().”
  + `tf.compat.v1.disable_eager_execution()`
  + https://stackoverflow.com/questions/57206247/how-to-fix-runtimeerror-the-session-graph-is-empty-add-operations-to-the-grap