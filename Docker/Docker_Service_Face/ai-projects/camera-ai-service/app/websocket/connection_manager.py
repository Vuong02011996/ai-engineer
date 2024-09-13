from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket,company_id):
        await websocket.accept()
        if company_id in self.active_connections:
            self.active_connections[company_id].append(websocket)
        else:
            self.active_connections[company_id] = [websocket]

    def disconnect(self, websocket: WebSocket):
        for key, value in self.active_connections.items():
            if websocket in value:
                value.remove(websocket)
                break

    async def send_company_message_txt(self, company_id: str, message: str):
        print(self.active_connections)
        if company_id in self.active_connections:
            for connection in self.active_connections[company_id]:
                print("sending message")
                await connection.send_text(message)

    async def send_company_message_json(self, company_id: str, message: dict):
        if company_id in self.active_connections:
            for connection in self.active_connections[company_id]:
                await connection.send_json(message)


connection_manager = ConnectionManager()
