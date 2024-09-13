import asyncio
import threading
import time

import requests

from app.common.constants.enums import ProcessStatus
from app.common.observer.connect_rabbitmq.observer_connect_rabiitmq import (
    ObserverConnectRabbitMQ,
)
from app.models import Server, Service
from app.schemas.process_schemas import ProcessRun
from app.services.service_services import service_services
from app.services.process_services import process_services
from app.websocket.web_socket_super_admin import web_socket_super_admin


class CheckConnectObserver(ObserverConnectRabbitMQ):
    list_service = {}

    def __init__(self):
        data_service: list[Service] = service_services.get_services()
        for service in data_service:
            server: Server = service.server
            self.list_service[server.ip_address + "_" + str(service.port)] = time.time()

        threading.Thread(target=self.check_offline_server, daemon=True).start()

    def update(self, message):
        threading.Thread(target=self.update_th, args=(message,), daemon=True).start()

    def update_th(self, message):
        # print(f"received message: {message}")
        if "ip" not in message or "port" not in message:
            return
        self.list_service[str(message["ip"]) + "_" + str(message["port"])] = time.time()
        ip = message["ip"]
        port = message["port"]
        try:
            service = service_services.update_status_by_ip_port(
                ip=message["ip"], port=message["port"], status=True
            )
            asyncio.run(
                web_socket_super_admin.send_company_message_json(
                    {
                        "type": "ALIVE_SERVICE",
                        "data": {"id": str(service.id), "is_alive": True},
                    }
                )
            )
            if "data" not in message:
                return
            list_process = process_services.get_by_service_id(service_id=str(service.id))
            obj_process = {}
            obj_debug = {}
            for process in list_process:
                obj_process[str(process.id)] = process.isEnable
                obj_debug[str(process.id)] = process.is_debug

            for key in message["data"]:
                if key not in obj_process:
                    if obj_process[key] is True:
                        url = f"http://{ip}:{port}/kill"
                        try:
                            requests.post(url, json={"process_id": key}, timeout=2)
                        except Exception:
                            pass
                    continue
                else:
                    status = (
                        ProcessStatus.start
                        if message["data"][key] is True
                        else ProcessStatus.stop
                    )
                    process_services.update_status_by_id(key, status)
                    if status == ProcessStatus.stop:
                        url = f"http://{ip}:{port}/kill"
                        try:
                            requests.post(url, json={"process_id": key}, timeout=2)
                        except Exception:
                            pass
                        # enable process
                        data_send = {"process_id": key}
                        data_send["is_debug"] = obj_debug[key]
                        if obj_process[key] is True:
                            data_r = process_services.run_process(obj_in=ProcessRun(**data_send), is_router=False)

                    del obj_process[key]

            for key in obj_process:
                process_services.update_status_by_id(key, ProcessStatus.stop)
                if obj_process[key] is True:
                    data_send = {"process_id": key}
                    data_send["is_debug"] = obj_debug[key]
                    data_r = process_services.run_process(obj_in=ProcessRun(**data_send), is_router=False)



        except Exception as e:
            # print("Error CheckConnectObserver 14: ", e)
            pass

    def check_offline_server(self):
        while True:
            current_time = time.time()
            for key in list(self.list_service.keys()):  # Create a copy of the keys
                value = self.list_service.get(key)
                if value and current_time - value > 10:
                    # print(f"Server {key} is offline!")
                    del self.list_service[key]
                    try:
                        service = service_services.update_status_by_ip_port(
                            ip=key.split("_")[0], port=key.split("_")[1], status=False
                        )
                        asyncio.run(
                            web_socket_super_admin.send_company_message_json(
                                {
                                    "type": "ALIVE_SERVICE",
                                    "data": {"id": str(service.id), "is_alive": False},
                                }
                            )
                        )
                        process_services.update_status_by_service_id(
                            service_id=str(service.id), status=ProcessStatus.stop
                        )
                    except Exception as e:
                        # print("Error CheckConnectObserver: ", e)
                        pass

            time.sleep(5)


check_connect_observer = CheckConnectObserver()
