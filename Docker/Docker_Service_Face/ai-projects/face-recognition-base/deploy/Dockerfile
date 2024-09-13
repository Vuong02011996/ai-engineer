FROM ubuntu:18.04
# System packages
RUN apt-get update && apt-get install -y wget htop python3-dev libgl1-mesa-dev libglib2.0-0 nano iputils-ping

# Install miniconda to /miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/root/miniconda3/bin:${PATH}"
RUN conda create -y -n clover python=3.8
RUN mkdir "clover_app"
COPY .. clover_app/
WORKDIR clover_app
RUN bin/bash -c "source activate clover && pip install -r requirements.txt && python server.py"

#  sudo docker build -f Dockerfile -t clover:1.0 . \
#  sudo docker run --net=host --restart=always --name clover_v1.0 -it clover:1.0