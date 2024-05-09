import grpc
from concurrent import futures
from Socket_WebSocket_Http_grpc.Using_GRPC.generate_code_for_grpc import api_pb2, api_pb2_grpc
from shm.reader import SharedMemoryFrameReader
from yolov5_detect_image import Y5Detect
import time


class YOLOv5Servicer(api_pb2_grpc.YOLOv5Servicer):
    def __init__(self):
        self.dic_key = {}
        self.y5_model = Y5Detect(
            weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt"
        )

    def Predict(self, request, context):
        share_key = request.share_key
        if share_key != "" and share_key is not None:
            if share_key not in self.dic_key:
                self.dic_key[share_key] = SharedMemoryFrameReader(share_key)

            frame_rgb = self.dic_key[share_key].get()
            boxes, labels, scores, detections_sort = self.y5_model.predict_sort(frame_rgb, label_select=["head"])

            box_messages = [api_pb2.Box(coordinates=box) for box in boxes]
            detections_sort_messages = [api_pb2.Box(coordinates=box) for box in detections_sort]
            response = api_pb2.Response(
                boxes=box_messages,
                labels=labels,
                scores=scores,
                detections_sort=detections_sort_messages
            )
            return response
        else:
            return api_pb2.Response()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_YOLOv5Servicer_to_server(YOLOv5Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
