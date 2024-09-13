FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        ffmpeg \
        libsm6 \
        libxext6 \
        git \
        cmake && \
    rm -rf /var/lib/apt/lists/*

RUN git clone --branch v19.24.6 --depth 1 https://github.com/davisking/dlib.git && \
    cd dlib && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . && \
    cd .. && \
    python setup.py install && \
    cd .. && \
    rm -rf dlib

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade -r requirements.txt

COPY ./ /app

ENTRYPOINT [ "bash" ]
CMD ["entrypoint.sh"]

