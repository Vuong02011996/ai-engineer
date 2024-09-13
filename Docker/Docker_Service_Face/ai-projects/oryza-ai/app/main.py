import threading
from fastapi import FastAPI
import os
from contextlib import asynccontextmanager

from app.api.main import api_router
from app.common.utils.check_alive_server import CheckAliveServer
from app.rabbitmq.start_mq import StartMQ
from app.api.routes.websocket_routes import router as api_router_ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("temp"):
        os.makedirs("temp")
    StartMQ().start()
    threading.Thread(target=CheckAliveServer().start, args=(), daemon=True).start()
    yield
    print("Shutting down the server")
    # os.system("rm -rf temp")


app = FastAPI(
    title="Oryza AI FastAPI Backend",
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router_ws, prefix="/ws")
