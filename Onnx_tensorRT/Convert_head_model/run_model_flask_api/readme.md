# Test performance when call api many times
+ Call one time cost: 0.01s
+ Call 2 time: ~0.02s
+ Call 3 time: 0.03s
+ Call 5 time: 0.045s
+ Call 10 time: 0.07 - 0.09s
+ Call 50 time: 0.11-0.13s
+ Call 100 time: 0.11-0.13s
+ Call 1000 time: 0.11-0.13s

+ All time in api only cost: y5_model.predict_sort cost:  0.0077342987060546875
# If not service model head
+ init model cost 2G VRAM
+ Run one cam cost > 1G RAM GPU
=> Can't use
+ Model head open when using service: only 300MB for one model.
+ => each camera using one port head detection 