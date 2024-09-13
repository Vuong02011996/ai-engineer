from fastapi import WebSocket


class WebSocketSuperAdmin:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_company_message_txt(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_company_message_json(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


web_socket_super_admin = WebSocketSuperAdmin()
