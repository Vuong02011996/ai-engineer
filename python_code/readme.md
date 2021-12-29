# New Syntax
1. assert
    + The assert statement exists in almost every programming language. It helps detect problems early in your program, where the cause is clear, rather than later when some other operation fails
        [link](https://stackoverflow.com/questions/5142418/what-is-the-use-of-assert-in-python)
    + code:
   ```python
    assert len(boxes_face) == len(track_ids)
    ```
   
2. What does the star and doublestar operator mean in a function call?
   1. Ref [here](https://stackoverflow.com/questions/2921847/what-does-the-star-and-doublestar-operator-mean-in-a-function-call)
   2. The single star * unpacks the sequence/collection into positional arguments.
   3. The double star ** does the same, only using a dictionary
2. Thread one arguments
    + t = KThread(target=main, args=(input_path,))
    + Have "," after args
    + [link](https://stackoverflow.com/questions/37116721/typeerror-in-threading-function-takes-x-positional-argument-but-y-were-given)
# Numpy 
