import grpc
import numpy as np

from Socket_WebSocket_Http_grpc.Using_GRPC.generate_code_for_grpc import api_pb2, api_pb2_grpc
from shm.writer import SharedMemoryFrameWriter
import cv2

# image_bgr = cv2.imread("/home/oryza/Pictures/image_test/couple.jpg")
image_bgr = cv2.imread("/home/oryza/Pictures/image_test/img3.jpg")
frame_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def test_api_model():
    channel = grpc.insecure_channel('localhost:50051')
    stub = api_pb2_grpc.YOLOv5Stub(channel)

    process_id = "604ef817ef7c20fc5e52a20d"
    shm_w1 = SharedMemoryFrameWriter(process_id)
    shm_w1.add(frame_rgb)

    request = api_pb2.Request(share_key=process_id)
    response = stub.Predict(request)
    print("response: ", response)
    # Initialize an empty list to store the converted boxes
    boxes = []
    labels = []
    scores = []
    detections_sort = []
    # Iterate over the boxes in the response
    for i in range(len(response.boxes)):
        # Extract the coordinates from the box message and append them to the boxes list
        coordinates = list(response.boxes[i].coordinates)
        boxes.append(coordinates)
        labels.append(response.labels[i])
        scores.append(response.scores[i])
        coor_detect_sort = list(response.detections_sort[i].coordinates)
        detections_sort.append(coor_detect_sort)

    # Print the resulting list of boxes

    boxes = np.array(boxes, dtype=int)
    detections_sort = np.array(detections_sort)
    print(boxes)


if __name__ == '__main__':
    test_api_model()