# Hardware 
+ GPU : NVIDIA Corporation TU106 [GeForce RTX 2070]
  + `sudo lshw -C display`
  + 8G VRAM
  + Clock: 33MHz 
+ CPU: 24G RAM 
  + `lscpu`
  + 12th Gen Intel(R) Core(TM) i5-12400
  + Thread(s) per core:                 2
  + Core(s) per socket:                 6
  + Socket(s):                          1
  + CPU MHz:                            2500.000
  + CPU max MHz:                        4400,0000
  + CPU min MHz:                        800,0000

# Model 
+ Face detection and recognition: [link](https://repo.oryza.vn/oryza/ai/face-recognition-base/-/tree/master/core/models_local)
  + Init: 2,5G VRAM GPU
+ Head : [link](https://repo.oryza.vn/oryza/ai/face-recognition-base/-/tree/master/core/models_local/head_detection/yolov5_detect)
  + Run in service: 400M VRAM GPU
  + Run in local(one cam init one time): 
# Performance
+ 1 camera: realtime

+ Run 4 camera:
  + Duplicate model 
    + 2.5G x 2 VRAM GPU Face
    + 400M x 2 VRAM GPU Head service 
  + Skip frame 4( ignore 3 frame )
  + Almost realtime.

+ Run 4 camera:
  + Duplicate model 
    + 2.5G x 1 VRAM GPU Face
    + 400M x 2 VRAM GPU Head run local, init with camera. 
  + Skip frame 4( ignore 3 frame )
  + Almost realtime.

+ Increase conf_threshold of head detection self.conf_threshold = 0.3 -> 0.6: 
  + Decrease accuracy of tracking
  + Increase speed of model Face detection , more head more call api.
## Run 8 cam:
+ Combine:
  + 2 model service face: 4 cam 1 model
  + 2 model service head: 4 cam 1 model
  + head detection 0.6
  + frame step 4
  + Step after tracking 4.
=> not realtime.
  
## Run 4 cam:
+ Combine:
  + 2 model service face: 2 cam 1 model
  + 2 model service head: 2 cam 1 model
  + head detection 0.6
  + frame step 4
  + Step after tracking 4.
=> realtime but result not good.

# Test performance on video
   + Test on input_path = "/home/oryza/Videos/Video_test_acc2.mp4"
   + One service head: 5000
   + One service face: 18081
   + match_identity[idx]["distance"] < 0.5 (need test again) => Thieu Khoi, Vinh 17
     + 0.6 : detect Khoi, Vinh 17 FPS36.54 => choice
## Run one cam
### confidence head detect
+ 0.8 => 41FPS
+ 0.4 => 35FPS : detect head sai nhieu
+ 0.5 => 36FPS : detect oke -> tracking oke(the same id 8 with me) -> choice -> can test nhieu lan voi cac video khac nhau.
  + 0.6 => 37FPS: detect oke -> NOT OKE id 7 -> 42 with me

### extend_bbox current 10 sometime face detect not good -> decrease accuracy
+ The same confidence head is 0.6
  + 50 => FPS 35
  + 10 => FPS 37.5
+ The same confidence head is 0.5
  + 10 => FPS 36.75
### track have name, no detect face: xoa track khi track da co name(khong xu li face detect)
+ FPS 43

## Run 2 cam one 5000/18081
+ head_detect cost:  0.04 - 0.06
+ detect_face_bbox_head cost:  0.03 - 0.09
### confidence head detect
+ 0.5 => 20FPS : detect oke -> tracking oke(the same id 8 with me) -> choice -> can test nhieu lan voi cac video khac nhau.

### extend_bbox current 10 sometime face detect not good -> decrease accuracy
+ The same confidence head is 0.5
  + 10 => FPS 20

### track have name, no detect face: xoa track khi track da co name(khong xu li face detect)
+ FPS 27

## Run 2 cam on 5000/18081 and run 2 cam one on 5001/18083
+ FPS 18
+ Frame step 2 before tracking: FPS 25 BUT acc tracking decrease 8 track id -> 12

## Run 2 cam on 18081 and run 2 cam one on 18083 and each cam each port head(5000-5003)
+ FPS 20:
  + head_detect cost:  0.03 - 0.09
  + detect_face_bbox_head cost:  0.01031041145324707 - ok
  + extract embedding cost:  0.00013947486877441406 - ok
  + head_detect cost:  0.048650264739990234 



# Accuracy
+ model face recognition:
  + w600k_mbf: video acc2: 3 person: 
  + glintr100: video acc2: 7 person - FPS: 34