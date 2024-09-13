# Combine face detection and recognition
+ [insightface](https://github.com/deepinsight/insightface)
  + https://github.com/deepinsight/insightface/blob/master/recognition/arcface_torch/eval/verification.py
+ [InsightFace-REST](https://github.com/SthPhoenix/InsightFace-REST)
  + Requirements
    + Docker 
    + Nvidia-container-toolkit 
    + Nvidia GPU drivers (470.x.x and above)
  + Build successfully. container insightface-rest-gpu0-trt
  + Run and Start 
    + Error: docker: Error response from daemon: could not select device driver "" with capabilities: [[gpu]]
      + Install Nvidia-container-toolkit [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
  + Swagger API: http://0.0.0.0:18081/
# Convert np.array to base64 string
+ Step : convert to bytes -> encode bytes - base64 -> decode bytes of base64 - string. 

+ Convert to bytes have two options:
  + Save image and read again [link](https://stackoverflow.com/questions/50444141/how-to-encode-and-decode-between-base64-string-and-numpy-array)
  + Immediate: 
    ```python
        success, encoded_image = cv2.imencode('.png', image_face)
        image_face = encoded_image.tobytes()
    ```
# Performance InsightFace-REST
+ Two model face detection and face recognition is converted to TensorRT(Triton) and service to API. 
+ Model detection: retinaface_r50_v1
+ Model recognition: arcface_r100_v1

  *Image is converted to base64 string*
  ```python
  def file2base64(path):
      with open(path, mode='rb') as fl:
          encoded = base64.b64encode(fl.read()).decode('ascii')
          return encoded
  
  
  def extract_vecs(ims, max_size=[200, 200]):
      target = [file2base64(im) for im in ims]
      # req = {"images": {"data": target}, "max_size": max_size, "embed_only": True}
      req = {"images": {"data": target}, "embed_only": True}
      start_time = time.time()
      resp = requests.post('http://localhost:18081/extract', json=req)
      data = resp.json()
      print("Reponse cost: ", time.time() - start_time)
      return data
  ```

## Face detection
*Image resize to (200,200)*
    ```python
    req = {"images": {"data": target}, "max_size": max_size, "extract_embedding": False}
    ```
+ Test in one image: 0.01s - 0.02s(50FPS)
+ Test batch with 10 image: 0.06s - 0.07s(16FPS) - need test again without service.
## Face recognition
*Image size (112,112)*
    ```python
    req = {"images": {"data": target}, "embed_only": True}
    ```
+ Test in one image: 0.012s - 0.02s(50FPS)
+ Test batch with 10 image: 0.06s - 0.07s(16FPS) - need test again without service.
### Both detection & recognition
    ```python
    req = {"images": {"data": target}, "max_size": max_size}
    ```
+ Test in one image: 0.018s - 0.03s(~50FPS)
+ Test batch with 10 image: 0.13s - 0.15s(6 - 10FPS)
+ Test one image size 1400*640(thresh = 0.05): 0.05s
## Bug when detect image batch 
```commandline
target = [list image base64]
 req = {"images": {"data": target}, "threshold": det_threshold, "return_landmarks": True, "embed_only": False,
               "extract_embedding": False}
resp = requests.post(self.api_insightface, json=req)
data = resp.json()
```

# Performance ArceFaceTorch in InsightFace
+ [ArceFaceTorch-Batch](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)
+ Model recognition: ms1mv3_arcface_r50_fp16
+ Test in one image: 0.1s - 0.2s(~10FPS)
+ Test batch with 10 image: 0.6s - 0.8s(~1FPS)
  + Code 
    `````python
    weight = "/home/vuong/Desktop/Project/Github_ref/insightface/recognition/arcface_torch/ms1mv3_arcface_r50_fp16/backbone.pth"
    net = get_model('r50', fp16=False)
    net.load_state_dict(torch.load(weight))
    net.eval()
    @torch.no_grad()
    def inference_batch(list_images_path):
        batch_im = None
        for img in list_images_path:
            if img is None:
                print('read {} error'.format(img))
                img = np.random.randint(0, 255, size=(112, 112, 3), dtype=np.uint8)
            else:
                img = cv2.imread(img)
                img = cv2.resize(img, (112, 112))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = np.transpose(img, (2, 0, 1))
  
            if batch_im is None:
                batch_im = img[None, :, :, :]
            else:
                batch_im = np.vstack((batch_im, img[None, :, :, :]))
  
        img = torch.from_numpy(batch_im).float()
        img.div_(255).sub_(0.5).div_(0.5)
        feat = net(img).numpy()
  
    `````
    
# Performance RetinaTorch in DSFD-Pytorch-Inference
+ [DSFD-Pytorch-Inference-batch size](https://github.com/hukkelas/DSFD-Pytorch-Inference/tree/2bdd997d785e20ea39a911e9b3c451b7cdd3b152)
+ (DSFD)Dual Shot Face Detector
+ [paper-2019](https://arxiv.org/pdf/1810.10220.pdf)
+ *Using A High-Performance Pytorch Implementation* in [here](https://github.com/Tencent/FaceDetection-DSFD)
+ Model : RetinaNetResNet50, max_resolution=200
*Inage size (200,200)*
+ Test one image : 0.008s (125FPS)
+ Test batch 10 images: 0.038s 26FPS.
  + Code
      ```python
      detector = face_detection.build_detector(
          "RetinaNetResNet50",  # RetinaNetResNet50, RetinaNetMobileNetV1
          max_resolution=200
      )
    
    def test_detect_batch():
      impaths = "/home/vuong/Desktop/Project/GG_Project/clover/core/main/face_detect/image_head"
      impaths = glob.glob(os.path.join(impaths, "*.png"))
      impaths = impaths[:10]
      # impaths = [impaths[0]]
      for i, impath in enumerate(impaths):
          if impath.endswith("out.jpg"):
              continue
          im = cv2.imread(impath)
          im = cv2.resize(im, (200, 200), interpolation=cv2.INTER_AREA)
          im = im[:, :, ::-1]
          if i == 0:
              batch_im = im[None, :, :, :]
          else:
              # batch_im = np.concatenate((batch_im, im), axis=0)
              batch_im = np.vstack((batch_im, im[None, :, :, :]))
      t = time.time()
      dets = detector.batched_detect_with_landmarks(batch_im)
      print(f"Detection time: {time.time() - t:.3f}")
      ```
    
+ TesorRT: Not yet using.
+ Code
    ```python
    from face_detection.retinaface.tensorrt_wrap import TensorRTRetinaFace
    
    inference_imshape =(480, 640) # Input to the CNN
    input_imshape = (1080, 1920) # Input for original video source
    detector = TensorRTRetinaFace(input_imshape, imshape)
    boxes, landmarks, scores = detector.infer(image)
    ```