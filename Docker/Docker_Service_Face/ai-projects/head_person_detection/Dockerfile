FROM ultralytics/yolov5:latest

WORKDIR /app/src/head_person

RUN pip install fastapi==0.111.0 uvicorn==0.30.1 pydantic==2.7.4 posix_ipc==1.1.1 python-dotenv==0.19.0 gunicorn==23.0.0

COPY ./ /app/src/head_person

ENTRYPOINT [ "bash" ]
CMD ["entrypoint.sh"]
