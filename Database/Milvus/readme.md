# Benchmarking between milvus 0.10.6 vs milvus 2.0(ORM->slower)
+ Number of vector in collection: 3000
+ Dim: 512
+ gpu_search_threshold: 5
## Search 1 vector(CPU)
+ 0.10.6: 0.006s
+ 2.0: 0.03s

## Search 10 vector(GPU)
+ 0.10.6: 0.003s
+ 2.0: 0.03s