import sys
import os
import json
import numpy as np
import time
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from shm.reader import SharedMemoryFrameReader
from yolov5_detect_image import Y5Detect
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allowing CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dic_key = {}

y5_model = Y5Detect(
    weights="model_head/y5headbody_v2.pt"
)

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


@app.post("/yolov5/predict/share_memory")
async def retina(share_key: str = Body(..., embed=True)):
    # print("share_key: ", share_key)
    start_time = time.time()
    if share_key != "" and share_key is not None:
        if share_key not in dic_key:
            dic_key[share_key] = SharedMemoryFrameReader(share_key)

        # frame_rgb = await dic_key[share_key].get()
        frame_rgb = dic_key[share_key].get()
        boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["body"])
        # labels = await y5_model.predict_sort(frame_rgb, label_select=["head"])

        data_out = {
            "boxes": boxes,
            "labels": labels,
            "scores": scores,
            "detections_sort": detections_sort,
        }
        # data_out = {}
        # print("y5_model.predict_sort cost: ", time.time() - start_time)
        return json.dumps(data_out, cls=NumpyEncoder)
    else:
        return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT"), log_level="warning")
