# Run cvat server and ui with docker compose
+ https://docs.cvat.ai/docs/administration/basics/installation/
```
git clone https://github.com/cvat-ai/cvat
cd cvat/
export CVAT_HOST=127.0.0.1
docker compose up -d
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
```

# Run cvat server using AI tools
## Nulcio - the same triton(server infer models)
+ Nuclio được phát triển bởi Iguazio, một công ty công nghệ tập trung vào việc cung cấp các giải pháp dữ liệu và trí tuệ nhân tạo
+ Nuclio giúp đơn giản hóa việc xây dựng và chạy các ứng dụng mà không cần quản lý cơ sở hạ tầng phức tạp.
+ Ra đời 2017.


+ https://docs.cvat.ai/docs/administration/advanced/installation_automatic_annotation/
```
# Start CVAT together with the plugin use for AI automatic annotation assistant.
docker compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml up -d

# Create account
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
admin
vanvuong0440@gmail.com
pass: 123

# install nuclio command 
wget https://github.com/nuclio/nuclio/releases/download/1.13.0/nuctl-1.13.0-linux-amd64
sudo chmod +x nuctl-1.13.0-linux-amd64
# If not dictionary local/bin, makde directory.
sudo ln -sf $(pwd)/nuctl-1.13.0-linux-amd64 /usr/local/bin/nuctl

# Build the docker image and run the container. After it is done, you can use the model right away in the CVAT.
## object detection
./serverless/deploy_cpu.sh serverless/openvino/omz/public/yolo-v3-tf
./serverless/deploy_cpu.sh serverless/onnx/WongKinYiu/yolov7/nuclio/

./serverless/deploy_gpu.sh serverless/pytorch/facebookresearch/sam/nuclio/

  # Using model yolov8 custom
  clone https://github.com/kurkurzz/custom-yolov8-auto-annotation-cvat-blueprint.git
  ./serverless/deploy_cpu.sh path/to/this/folder/

# Recreate to show ai tools
docker compose down
docker compose -f docker-compose.yml -f components/serverless/docker-compose.serverless.yml up -d
```

# Upload data with label to cvat 
(Should be test with some image to faster process)
+ Infer folder images need to label to file .txt with format yolo1.1 , every file image is one file label.
+ create folder data:
  + Copy all file label and file image (the same file name) to folder name: obj_train_data 
  + Create file obj.data save path
  + Create file obj.names to save classes
  + Create file train.txt with path to file image.
+ Zip folder data with command: `zip -r9 data.zip ./*` (don't using compress in ui ubuntu)
