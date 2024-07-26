import os
import shutil
import random
from sklearn.model_selection import train_test_split

prefix_path = "/home/oryza/Desktop/Data_Training/Loitering/yolov8_data/"
# Define paths
images_path = '/home/oryza/Desktop/Data_Training/Loitering/images_person/images_person'
labels_path = '/home/oryza/Desktop/Data_Training/Loitering/images_person_22_7/obj_Train_data'

train_images_path = f'{prefix_path}images/train'
val_images_path = f'{prefix_path}images/valid'
train_labels_path = f'{prefix_path}labels/train'
val_labels_path = f'{prefix_path}labels/valid'

# Create directories if they do not exist
os.makedirs(train_images_path, exist_ok=True)
os.makedirs(val_images_path, exist_ok=True)
os.makedirs(train_labels_path, exist_ok=True)
os.makedirs(val_labels_path, exist_ok=True)

# List all images and labels
images = sorted([f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])
labels = sorted([f for f in os.listdir(labels_path) if f.endswith('.txt')])

# Ensure corresponding images and labels exist
images = [f for f in images if f.replace('.jpg', '.txt').replace('.png', '.txt') in labels]

# Shuffle images and labels
random.seed(42)
random.shuffle(images)

# Split data into train and validation sets (80% train, 20% val)
train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

# Copy files to train and validation directories
for image in train_images:
    shutil.copy(os.path.join(images_path, image), os.path.join(train_images_path, image))
    shutil.copy(os.path.join(labels_path, image.replace('.jpg', '.txt').replace('.png', '.txt')),
                os.path.join(train_labels_path, image.replace('.jpg', '.txt').replace('.png', '.txt')))

for image in val_images:
    shutil.copy(os.path.join(images_path, image), os.path.join(val_images_path, image))
    shutil.copy(os.path.join(labels_path, image.replace('.jpg', '.txt').replace('.png', '.txt')),
                os.path.join(val_labels_path, image.replace('.jpg', '.txt').replace('.png', '.txt')))

# Write paths to coco.yaml file
coco_yaml_content = f"""
train: {train_images_path}  # train images (relative to 'path')
val: {val_images_path}  # val images (relative to 'path')

# Classes
names:
  0: person
"""

with open(f'{prefix_path}coco.yaml', 'w') as f:
    f.write(coco_yaml_content)

print("Data split and coco.yaml file created successfully!")
