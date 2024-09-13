from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.connection_manager import connection_manager
from app.websocket.web_socket_super_admin import web_socket_super_admin

router = APIRouter()


@router.websocket("/super_admin")
async def websocket_endpoint(websocket: WebSocket):
    await web_socket_super_admin.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await web_socket_super_admin.send_company_message_txt(f"You wrote: {data}")

    except WebSocketDisconnect:
        web_socket_super_admin.disconnect(websocket)


@router.websocket("/{company_id}")
async def websocket_endpoint(websocket: WebSocket, company_id: str):
    await  connection_manager.connect(websocket, company_id)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.register_event(websocket,data)

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
