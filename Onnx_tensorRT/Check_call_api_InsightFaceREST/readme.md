# If send 100 image send API to server not good
- Start more server with another port.
- Can switch GPU.

# Performance when call many times api at the same time - face detection have landmark - batch 10
+ Call one time cost: 0.01s
+ Call 2 time: ~0.02s
+ Call 3 time: 0.026s
+ Call 5 time: 0.045s
+ Call 10 time: 0.07 - 0.09s
+ Call 50 time: 0.11-0.13s
+ Call 100 time: 0.11-0.13s
+ Call 1000 time: 0.11-0.13s

# Performance when call many times api at the same time - face detection have landmark - batch 5
+ Call one time cost: 0.01s
+ Call 2 time: ~0.012s
+ Call 3 time: 0.018s
+ Call 5 time: 0.03s
+ Call 10 time: 0.04 - 0.05s
+ Call 50 time: 0.06-0.08s
+ Call 100 time: 0.06-0.08s
+ Call 1000 time: 0.06-0.08s

# Performance when call many times api at the same time - face detection have landmark - batch 1
+ Call one time cost: 0.01s
+ Call 2 time: ~0.01s
+ Call 3 time: 0.01s
+ Call 5 time: 0.02s
+ Call 10 time: 0.02 - 0.03s
+ Call 50 time: 0.03-0.04s
+ Call 100 time: 0.03-0.04s
+ Call 1000 time: 0.03-0.04s