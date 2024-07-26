import os
import cv2
from ultralytics import YOLO


def infer_and_save_yolo_format(model_path, image_folder, save_folder):
    model = YOLO(model_path)

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    save_image = False
    for image_name in os.listdir(image_folder):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, image_name)
            result = model(image_path)
            image = cv2.imread(image_path)

            save_path = os.path.join(save_folder, os.path.splitext(image_name)[0] + '.txt')
            with open(save_path, 'w') as f:
                for det in result[0].boxes:
                    cls = det.cls.item()
                    # if cls == 0.0:  # Adjust the class filter as needed
                    xmin, ymin, xmax, ymax = map(int, det.xyxy[0].tolist())
                    conf = det.conf.item()

                    # Save YOLO format: class x_center y_center width height
                    img_height, img_width = image.shape[:2]
                    x_center = (xmin + xmax) / 2 / img_width
                    y_center = (ymin + ymax) / 2 / img_height
                    width = (xmax - xmin) / img_width
                    height = (ymax - ymin) / img_height
                    f.write(f"{int(cls)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

                    # Optional: Draw bounding box and save the image
                    if save_image:
                        color = (0, 255, 0)
                        thickness = 2
                        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)
                        label = f'Class: {cls} Conf: {conf:.2f}'
                        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

            if save_image:
                # Optionally, save the image with drawn bounding boxes
                cv2.imwrite(os.path.join(save_folder, image_name), image)


def save_image_paths(image_folder, save_file, prefix):
    # Get the list of image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Open the save file in write mode
    with open(save_file, 'w') as file:
        for image_name in image_files:
            # Construct the full path for each image
            image_path = os.path.join(prefix, image_name)
            # Write the image path to the file
            file.write(f"{image_path}\n")


if __name__ == '__main__':
    image_folder = '/home/oryza/Desktop/Data_Training/Loitering/images_person/images_person'
    # Example usage
    # model_path = '/home/oryza/Desktop/Projects/Loiter_Detection/core/models_local/head_detection/yolov8_detection/head_peron_yolov8_v1.pt'
    # save_folder = '/home/oryza/Desktop/Data_Training/Loitering/images_person/labels'
    # infer_and_save_yolo_format(model_path, image_folder, save_folder)

    # Example usage
    save_file = '/home/oryza/Desktop/Data_Training/Loitering/images_person/data/train.txt'
    prefix = 'data/obj_train_data'
    save_image_paths(image_folder, save_file, prefix)
