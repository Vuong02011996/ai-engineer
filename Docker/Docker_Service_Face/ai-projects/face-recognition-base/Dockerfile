FROM python:3.8

WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ADD requirements.txt /app/requirements.txt
RUN pip install pip==21.1.1
RUN pip install --upgrade -r requirements.txt
COPY ./ /app

ENTRYPOINT [ "bash" ]
CMD ["entrypoint.sh"]
