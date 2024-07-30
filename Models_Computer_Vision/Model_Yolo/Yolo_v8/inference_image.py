from ultralytics import YOLO
import cv2


def infer_1():
    model = YOLO('models/model_Manh.pt')
    result = model('/home/oryza/Desktop/Projects/ai-engineer/Model_Yolo/images_test/body_test.png')
    for result in result[0].boxes.numpy():
        xyxy = result.xyxy[0]
        x1, y1, x2, y2 = map(float, xyxy)
        cls = int(result.cls[0])
        conf = float(result.conf[0])
        print("x1: ", x1, "y1: ", y1, "x2: ", x2, "y2: ", y2, "cls: ", cls, "conf: ", conf)


def infer_2():
    # model = YOLO('models/model_Manh.pt')
    model = YOLO('/Models_Computer_Vision/Model_Yolo/Yolo_v8/runs/detect/train4/weights/best.pt')

    image_path = '/Models_Computer_Vision/Model_Yolo/images_test/body_test.png'
    result = model(image_path)
    # Load the image with OpenCV
    image = cv2.imread(image_path)

    for det in result[0].boxes:
        cls = det.cls.item()  # Get Python number from tensor
        if cls == 1.0:
            # xmin, ymin, xmax, ymax = det.xyxy[0].tolist()  # Convert tensor to list for easier handling
            xmin, ymin, xmax, ymax = map(int, det.xyxy[0].tolist())  # Convert tensor to list and cast to int
            conf = det.conf.item()  # Get Python number from tensor

            print("x1: ", xmin, "y1: ", ymin, "x2: ", xmax, "y2: ", ymax, "cls: ", cls, "conf: ", conf)

            # Define the bounding box color and thickness
            color = (0, 255, 0)  # Green color
            thickness = 2

            # Draw the bounding box
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

            # Put class and confidence text
            label = f'Class: {cls} Conf: {conf:.2f}'
            cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    # Optionally, display the image
    cv2.imshow('Detected Objects', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_number_of_class():
    # Get the number of classes
    model = YOLO('models/model_Manh.pt')
    num_classes = model.model.yaml['nc']
    print(f"Number of classes: {num_classes}")


if __name__ == '__main__':
    infer_2()
    # get_number_of_class()