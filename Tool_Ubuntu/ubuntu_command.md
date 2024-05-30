
# show all environment in ubuntu
+ locate -b '\activate' | grep "/home"

# view all process running
+ sudo ps -au
+ nvtop

# Kill all process python
+ sudo pkill -9 python

scp  -r /home/sgtvt/Pictures/Data/image_detected_final sgtvt-dbwb@172.17.23.11:/home/sgtvt-dbwb/gtvt/data/thidiem_camera_data/files/diembienbao/Data 