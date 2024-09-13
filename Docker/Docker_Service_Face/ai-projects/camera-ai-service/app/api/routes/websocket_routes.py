from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.connection_manager import connection_manager

router = APIRouter()

@router.websocket("/add_user/{company_id}")
async def websocket_endpoint(websocket: WebSocket, company_id: str):
    await  connection_manager.connect(websocket, company_id)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_company_message_txt(company_id, f"You wrote: {data}")

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
