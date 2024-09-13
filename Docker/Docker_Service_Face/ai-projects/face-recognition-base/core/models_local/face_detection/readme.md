# Detect Face from image
## Pytorch retina
### Using lib
+ model download and save to .cache
+ [link](https://pypi.org/project/retinaface-pytorch/)
+ Detect good but time performance is not good.
  + 0.05s - 0.1s in each image have > 4, 5 head.
  + FPS < 20
  + No support batch size in current.
### Using repo github
+ [Repo-ternaus](https://github.com/ternaus/retinaface)
  + Run
    ```
      python -m torch.distributed.launch --nproc_per_node=1 retinaface/inference.py\
      -i /home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/image_head \
      -o /home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/output_test \
      -c /home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/pytorch_retinaface/retinaface/retinaface/configs/2020-07-20.yaml \
      -w /home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/pytorch_retinaface/models/resnet50_epoch149.ckpt
      ```
  + Some change:
    + Line 232  ```file_paths = list(args.input_path.rglob("*.png"))```
  + Issue: 
    + How to run python -m torch.distributed.launch in to test model.
+ [Repo-origin](https://github.com/biubug6/Pytorch_Retinaface/blob/master/test_widerface.py#L16)
  + Not using batch size.

# A High-Performance Pytorch Implementation of the paper "DSFD: Dual Shot Face Detector" (CVPR 2019)
+ [Repo-batch-size](https://github.com/hukkelas/DSFD-Pytorch-Inference/tree/2bdd997d785e20ea39a911e9b3c451b7cdd3b152)
  + FPS one image 4- 10 head: 0.02-0.05s
  + Using: RetinaNetMobileNetV1

## Facenet
+ [link](https://github.com/timesler/facenet-pytorch)