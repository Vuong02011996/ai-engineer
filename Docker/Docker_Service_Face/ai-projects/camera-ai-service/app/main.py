import logging

from fastapi import FastAPI
import os
import socket
import time
import threading

from app.api.main import api_router
from app.api.routes.process_routes import get_all_process_status

# from app.rpc_server.mq_service import MQService
from app.services.pika_publisher import pika_publisher
from app.api.routes.websocket_routes import router as api_router_ws

app = FastAPI(
    title="Oryza Camera AI FastAPI Backend",
    docs_url="/",
)


def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipV4 = s.getsockname()[0]
    s.close()
    return ipV4


def send_info_connection():
    ip = get_ipv4_address()
    while True:
        list_process = get_all_process_status()
        data_send = {"ip": ip, "port": 8000, "data": list_process}
        # logging.info(f"Send info connection: {data_send}")
        pika_publisher.send_to_rbmq(data_send, "CHECK_STATUS_SERVER_EXCHANGES")
        time.sleep(5)


app.include_router(api_router)
app.include_router(api_router_ws, prefix="/ws")


# def init_rpc():
#     mq_service = MQService()
#     mq_service.listen()


@app.on_event("startup")
async def startup_event():
    if not os.path.exists("temp"):
        os.makedirs("temp")
    print("Starting publisher connection...")
    threading.Thread(target=send_info_connection, daemon=True).start()
    # threading.Thread(target=init_rpc, daemon=True).start()
