import onnxruntime
import numpy as np
import cv2

from Onnx_tensorRT.Convert_head_model.run_model_origin.utils.general import check_img_size, non_max_suppression, scale_coords

# Load the ONNX model
onnx_model_path = 'yolov5.onnx'
ort_session = onnxruntime.InferenceSession(onnx_model_path)

# Define the class names
class_names = ['body', 'head']  # Define your class names here
label_select = ['head', 'body']
# Preprocess input image
def preprocess_image(image):
    image = cv2.resize(image, (640, 640))
    image = image.transpose(2, 0, 1)  # Channels-first
    image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Perform inference
def inference(image):
    input_image = preprocess_image(image)
    ort_inputs = {ort_session.get_inputs()[0].name: input_image}
    ort_outs = ort_session.run(None, ort_inputs)

    # Process the outputs
    detections = ort_outs[0]
    detections = non_max_suppression(detections, 0.3, 0.45)

    # Apply NMS
    bboxes = []
    labels = []
    scores = []
    for det in detections:  # detections per image
        if det is not None and len(det):
            # print(det)
            for box in det:
                x1, y1, x2, y2, conf = box[:5]  # Extract bounding box coordinates and confidence score
                cls = int(box[5])
                label = class_names[int(cls)]
                if label in label_select:
                    bboxes.append([int(x1), int(y1), int(x2), int(y2)])
                    labels.append(label)
                    scores.append(float(conf))

    return bboxes, labels, scores

# Example inference on an image
# image_path = '/home/oryza/Pictures/image_test/Truc.jpg'  # Provide the path to your input image
image_path = '/home/oryza/Pictures/image_test/test.png'  # Provide the path to your input image
image_bgr = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
result = inference(image_rgb)

print(result)  # Print the inference results
