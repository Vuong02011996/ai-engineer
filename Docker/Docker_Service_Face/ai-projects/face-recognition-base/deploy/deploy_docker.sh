#! /bin/bash

sudo docker build -f Dockerfile -t clover:1.0 .
sudo docker run --net=host --restart=always --name clover_v1.0 -it clover:1.0