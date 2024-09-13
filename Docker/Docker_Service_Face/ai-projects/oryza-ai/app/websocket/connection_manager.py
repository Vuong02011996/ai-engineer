import json

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.list_event_register = {}
        self.list_camera_register = {}

    async def connect(self, websocket: WebSocket, company_id):
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

        if websocket in self.list_event_register:
            del self.list_event_register[websocket]

        if websocket in self.list_camera_register:
            del self.list_camera_register[websocket]

    async def register_event(self, webSocket, data):
        try:
            data = json.loads(data)
            if "events" in data:
                if type(data["events"]) == list:
                    self.list_event_register[webSocket] = data["events"]
            if "cameras" in data:
                if type(data["cameras"]) == list:
                    self.list_camera_register[webSocket] = data["cameras"]
        except Exception as e:
            print("Error register_event: ", e)

    # async def register_camera(self, webSocket, data):
    #     try:
    #         data = json.loads(data)
    #         if "cameras" in data:
    #             if type(data["cameras"]) == list:
    #                 self.list_camera_register[webSocket] = data["cameras"]
    #     except Exception as e:
    #         print("Error register_camera: ", e)

    async def send_company_message_txt(self, company_id: str, message: str):
        if company_id in self.active_connections:
            for connection in self.active_connections[company_id]:
                await connection.send_text(message)

    async def send_company_message_json(self, company_id: str, message: dict):
        if company_id in self.active_connections:
            for connection in self.active_connections[company_id]:
                check_connection_event= connection in self.list_event_register
                check_connection_camera= connection in self.list_camera_register

                # """có trong cả 2 list"""
                if check_connection_event and check_connection_camera:
                    if "type_service" in message and message["type_service"] in self.list_event_register[connection]:
                        if "data" in message:
                            data = message["data"]
                            if "camera_id" in data and data["camera_id"] in self.list_camera_register[connection]:
                                await connection.send_json(message)
                # """có trong list event"""
                elif check_connection_event:
                    if "type_service" in message and message["type_service"] in self.list_event_register[connection]:
                        await connection.send_json(message)
                # """có trong list camera"""
                elif check_connection_camera:
                    if "data" in message :
                        data = message["data"]
                        if "camera_id" in data and data["camera_id"] in self.list_camera_register[connection]:
                            await connection.send_json(message)
                # """không có trong cả 2 list"""
                else:
                    await connection.send_json(message)



connection_manager = ConnectionManager()
