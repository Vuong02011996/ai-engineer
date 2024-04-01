
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import json
import numpy as np

from shm.reader import SharedMemoryFrameReader

sys.path.append("../../Convert_head_model/run_model_origin")
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import Y5Detect

app = Flask(__name__)
CORS(app)

dic_key = {}


y5_model = Y5Detect(
    weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt")

class_names = y5_model.class_names


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route("/yolov5/predict/share_memory", methods=["POST"])
def retina():
    # get the data from request
    if request.headers['Content-Type'] == 'application/json':
        # If content type is JSON
        request_data = request.json
        share_key = request_data.get("share_key")
        # Handle the share_key as needed
    elif request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        # If content type is form data
        share_key = request.form.get("share_key")
        # Handle the share_key as needed
    else:
        print("error Unsupported Media Type 415")
        return []

    # Process share_key or return a response

    print("share_key: ", share_key)
    # share_key = "604ef817ef7c20fc5e52a20d"

    if share_key != "" and share_key is not None:
        if not (share_key in dic_key):
            dic_key[share_key] = SharedMemoryFrameReader(share_key)

        frame_rgb = dic_key[share_key].get()
        boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["head"])

        data_out = {
            "boxes": boxes,
            "labels": labels,
            "scores": scores,
            "detections_sort": detections_sort,
        }
        data_out = json.dumps(data_out, cls=NumpyEncoder)
        return data_out


if __name__ == "__main__":
    MODEL_HOST = "0.0.0.0"
    MODEL_PORT = 5000
    # app.run(host=os.getenv("MODEL_HOST"), port=int(os.getenv("MODEL_PORT")), threaded=False, debug=False)
    app.run(host=MODEL_HOST, port=int(MODEL_PORT), threaded=False, debug=False)
