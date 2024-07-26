from ultralytics import YOLO

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from YAML
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
# model = YOLO("/home/oryza/Desktop/Projects/ai-engineer/Model_Yolo/Yolo_v8/runs/detect/train4/weights/last.pt")
# model = YOLO("yolov8n.yaml").load("yolov8n.pt")  # build from YAML and transfer weights

prefix_path = "/home/oryza/Desktop/Data_Training/Loitering/yolov8_data/"
# Train the model
results = model.train(data=f'{prefix_path}coco.yaml',
                      epochs=300,
                      imgsz=640,
                      cache=True,
                      verbose=True)

