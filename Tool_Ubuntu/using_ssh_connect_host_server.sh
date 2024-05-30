## Copy file from host OS to local OS
In local PC:
scp -P 9992 vuonglv@49.156.52.21:/workspace/vuonglv/Projects/Trafic_sign/Training/darknet/backup/yolo-obj_26000.weights /home/vuong/Desktop/Project_GG/traffic_sign/models/train_v0.2
## Copy folder (add option -r)
scp -r user@your.server.example.com:/path/to/foo /home/user/Desktop/

## Copy file from local OS to host OS
IN Local PC:
rsync -av -e "ssh -p 9992" -P /media/vuong/2E9C26383F5BCF48/Data_Image/test.txt vuonglv@49.156.52.21:/workspace/vuonglv/Projects/Trafic_sign/Training/darknet/data
OR:
scp -r /home/vuong/traffic_sign/Result_PC_AI_Team/10:01:02.544052/image_detected_final root@192.168.1.249:/root/gtvt/data/thidiem_camera_data/files/diembienbao/Data/
scp -P 9992 /home/vuong/Downloads/yolov4.conv.137 vuonglv@49.156.52.21:/workspace/vuonglv/Projects/Trafic_sign/Training/darknet

## Connect
ssh vuonglv@49.156.52.21 -p 9992
