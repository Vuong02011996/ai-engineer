import sys
import json
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shm.reader import SharedMemoryFrameReader
sys.path.append("../../Convert_head_model/run_model_origin")
from Onnx_tensorRT.Convert_head_model.run_model_origin.yolov5_detect_image import Y5Detect

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
    weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt"
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
async def retina(share_key: str):
    try:
        if share_key != "" and share_key is not None:
            if share_key not in dic_key:
                dic_key[share_key] = SharedMemoryFrameReader(share_key)

            frame_rgb = await dic_key[share_key].get()
            boxes, labels, scores, detections_sort = await y5_model.predict_sort(frame_rgb, label_select=["head"])

            data_out = {
                "boxes": boxes,
                "labels": labels,
                "scores": scores,
                "detections_sort": detections_sort,
            }
            return json.dumps(data_out, cls=NumpyEncoder)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("your_script_name:app", host="0.0.0.0", port=5001, log_level="info")
