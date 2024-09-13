import asyncio
import os

import time
import socket

from app.services.server_services import server_services
from app.websocket.web_socket_super_admin import web_socket_super_admin
import ping3


class CheckAliveServer():
    def check_ip_availability(self, ip):
        response = ping3.ping(ip, timeout=2)
        if response is not None:
            return True
        else:
            return False

    def start(self):

        while True:
            data = server_services.get_multi()
            for server in data:
                ip_address = server.ip_address
                id = server.id
                try:
                    # ping server
                    if self.check_ip_availability(ip_address):
                        server_services.update_server(id=id, data={'is_alive': True})
                        asyncio.run(web_socket_super_admin.send_company_message_json(
                            {"type": "ALIVE_SERVER", "data": {"id": str(id), "is_alive": True}}))
                    else:
                        server_services.update_server(id=id, data={'is_alive': False})
                        asyncio.run(web_socket_super_admin.send_company_message_json(
                            {"type": "ALIVE_SERVER", "data": {"id": str(id), "is_alive": False}}))
                except Exception as e:
                    continue

            time.sleep(10)
