# Face recognition difference with person reid
+ Face recognition get face -> embedding.
  + ArceFace
+ Person reid get body -> embedding.
  + [link](https://github.com/layumi/Person_reID_baseline_pytorch)
  + [link](https://github.com/KaiyangZhou/deep-person-reid)
# Face recognition
  + [Repo_super_star](https://github.com/ageitgey/face_recognition)
    + [Not suport batch](https://github.com/ageitgey/face_recognition/blob/87a8449a359fbc0598e95b820e920ce285b8a9d9/face_recognition/api.py#L203)
  + [face-net](https://github.com/timesler/facenet-pytorch)
  + [insightface](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)
    + [batch](https://github.com/deepinsight/insightface/blob/master/recognition/arcface_torch/eval/verification.py#L227)
# Aligned face 
+ [link](https://github.com/1adrianb/face-alignment)

# Performance 
## InsightFace 

Image size 112*112

+ Model Arcface Resnet50
  + Run one face cost ~0.17s 6FPS
  + Run 10 face with batch ~0.75s 2FPS
+ Model Arcface Resnet 18
  + Run one face cost ~0.05s 20FPS
  + Run 10 face with batch ~0.35s 4FPS