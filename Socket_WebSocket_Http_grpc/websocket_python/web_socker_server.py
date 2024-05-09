#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json
import numpy as np
import time

from shm.reader import SharedMemoryFrameReader
from yolov5_detect_image import Y5Detect


y5_model = Y5Detect(
    weights="/home/oryza/Desktop/Projects/ai-engineer/Onnx_tensorRT/Convert_head_model/run_model_origin/model_head/y5headbody_v2.pt"
)

class_names = y5_model.class_names
dic_key = {}


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


async def echo(websocket):
    async for share_key in websocket:
        print("share_key: ", share_key)
        data_out = {}
        if share_key != "" and share_key is not None:
            if share_key not in dic_key:
                dic_key[share_key] = SharedMemoryFrameReader(share_key)

            # frame_rgb = await dic_key[share_key].get()
            frame_rgb = dic_key[share_key].get()
            boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["head"])
            # labels = await y5_model.predict_sort(frame_rgb, label_select=["head"])

            data_out = {
                "boxes": boxes,
                "labels": labels,
                "scores": scores,
                "detections_sort": detections_sort,
            }
            # print(data_out)
            # data_out = {}
            # print("y5_model.predict_sort cost: ", time.time() - start_time)

        data_out = json.dumps(data_out, cls=NumpyEncoder)
        await websocket.send(data_out)

        # await websocket.send(message)


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())