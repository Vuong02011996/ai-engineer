FROM python:3.10
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN git clone --branch v19.24.6 --depth 1 https://github.com/davisking/dlib.git
RUN pip install cmake
RUN cd dlib && mkdir build && cd build && cmake .. && cmake --build .
RUN cd dlib && python setup.py install
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./ /app
ENTRYPOINT [ "bash" ]
CMD ["entrypoint.sh"]
