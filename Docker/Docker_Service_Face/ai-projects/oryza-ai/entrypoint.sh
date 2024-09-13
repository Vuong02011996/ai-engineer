#!/bin/bash

set -e

exec gunicorn --log-level INFO\
     -w 1\
     -k uvicorn.workers.UvicornWorker\
     --keep-alive 60\
     --timeout 60\
     app.main:app -b 0.0.0.0:8001
