#!/bin/bash

set -e

# Fix error on yolov5
sed -i 's/recompute_scale_factor=self.recompute_scale_factor)/# recompute_scale_factor=self.recompute_scale_factor\n)/' /opt/conda/lib/python3.10/site-packages/torch/nn/modules/upsampling.py

exec gunicorn --log-level INFO\
     -w 1\
     -k uvicorn.workers.UvicornWorker\
     --keep-alive 60\
     --timeout 60\
     main:app -b 0.0.0.0:$PORT
