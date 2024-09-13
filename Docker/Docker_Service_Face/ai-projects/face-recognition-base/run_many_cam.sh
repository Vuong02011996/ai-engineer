#!/bin/bash

# Run Python scripts in the background
#python3 vms_face_detection_model.py &
python /home/oryza/Desktop/Projects/Face_Detection/app/services/vms_face_detection/vms_face_detection_model.py &
python /home/oryza/Desktop/Projects/Face_Detection/app/services/vms_face_detection/vms_face_detection_model.py &
#python /home/oryza/Desktop/Projects/Face_Detection/app/services/vms_face_detection/vms_face_detection_model.py &

# Wait for all scripts to finish
wait

echo "All scripts have finished."