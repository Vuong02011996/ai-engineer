from requests.auth import HTTPDigestAuth
import requests
import xml.etree.ElementTree as ET
from fastapi import HTTPException
import json
import cgi
from io import BytesIO
from datetime import datetime
import os
from typing import Optional
import time
from app.schemas.hik_camera_schema import Camera
from app.schemas.process_schemas import Process
from app.core.config import settings
from app.common.utils import this_server_ip, get_logger
from app.services.minio_services import minio_services

logger = get_logger("hik_services")
noti_logger = get_logger("noti_parse")


class HIKServices:
    def get_host(self, ip_address: str, port: int | None = None) -> str:
        """Get the host with the port, if it exists."""
        if port:
            return f"http://{ip_address}:{port}"
        return f"http://{ip_address}"

    def get_update_noti_cn_url(self, ip_address: str, port: int | None = None) -> str:
        """Get the URL to update the notification channel of the Hikvision camera."""
        host = self.get_host(ip_address, port)
        return f"{host}/ISAPI/Event/notification/httpHosts/{settings.HIK_NOTI_CHANNEL}"

    def get_update_noti_cn_xml(self):
        """Get the XML to update the notification channel of the Hikvision camera."""
        ip_address = this_server_ip
        port = settings.SERVER_PORT
        server_notification_url = "/hik/notifications"
        xml = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <HttpHostNotification version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
            <id>{settings.HIK_NOTI_CHANNEL}</id>
            <url>{server_notification_url}</url>
            <protocolType>HTTP</protocolType>
            <parameterFormatType>XML</parameterFormatType>
            <addressingFormatType>ipaddress</addressingFormatType>
            <ipAddress>{ip_address}</ipAddress>
            <portNo>{port}</portNo>
            <httpAuthenticationMethod>none</httpAuthenticationMethod>
        </HttpHostNotification>
        """
        return xml

    def parse_response(self, response: str, field: str) -> str:
        """Get the value of a field from an XML response, if it succeeds."""
        root = ET.fromstring(response)
        return root.find(f"{{http://www.hikvision.com/ver20/XMLSchema}}{field}").text

    def check_alive(self, process: Process) -> bool:
        """
        Get the address the camera is currently sending notifications to.
        If the camera is sending notifications to this server, return True.
        Otherwise, return False. If the request fails, return False, too.
        """
        try:
            response = requests.get(
                url=self.get_update_noti_cn_url(process.ip_address, process.port),
                auth=HTTPDigestAuth(process.username, process.password),
                timeout=settings.REQUEST_TIMEOUT,
            )
        except Exception:
            return False

        if response.status_code == 200:
            # Get the address the camera is currently sending notifications to
            current_camera_noti_ip_address = self.parse_response(
                response.text, "ipAddress"
            )
            if current_camera_noti_ip_address == this_server_ip:
                return True
            return False

    def update_noti_channel(self, process: Process):
        """
        Update the notification channel of the Hikvision camera.
        """
        try:
            response = requests.put(
                url=self.get_update_noti_cn_url(process.ip_address, process.port),
                auth=HTTPDigestAuth(process.username, process.password),
                data=self.get_update_noti_cn_xml(),
                headers={"Content-Type": "application/xml"},
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                return True
            else:
                raise HTTPException(
                    status_code=response.status_code, detail=response.text
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_noti_channel(self, camera: Camera):
        """
        Remove this server's ip address from the camera's notification channel.
        """
        try:
            response = requests.delete(
                url=self.get_update_noti_cn_url(camera.ip_address, camera.port),
                auth=HTTPDigestAuth(camera.username, camera.password),
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return False

    def start_new_process(self, process: Process) -> bool:
        """
        Every time a process is started,  update the notification channel to this server.
        """
        return self.update_noti_channel(process)

    def stop_process(self, process: Process) -> bool:
        camera = Camera(
            username=process.username,
            password=process.password,
            ip_address=process.ip_address,
            port=process.port,
        )
        return self.delete_noti_channel(camera)

    def parse_event(self, message: str, list_ip_address: Optional[list[str]] = None):
        """Parse the event data from the Hikvision camera
        Returns:
            image_url: str
            user_id: str
            timestamp: str
        """
        # Parse the multipart/form-data request
        environ = {
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE": "multipart/form-data; boundary=boundary",
        }
        form = cgi.FieldStorage(fp=BytesIO(message), environ=environ)
        # Extract the JSON and image data

        alarm_result = None
        image_data: bytes = None
        if "alarmResult" in form:
            alarm_result = json.loads(form["alarmResult"].value)
        if "faceImage" in form:
            image_data = form["faceImage"].value

        # print(alarm_result)
        if not alarm_result:
            print(f"{int(time.time())} No alarm result found")
            return

        if not image_data:
            print(f"{int(time.time())} No image data found")
            return

        ip_address = alarm_result["ipAddress"]

        if ip_address not in list_ip_address:
            print(f"Camera {ip_address} not found in the list of ip address")
            return
        # Print the name and user_id
        alarm_result = alarm_result["alarmResult"][0]
        print("Got alarm result")

        if "targetAttrs" in alarm_result and "faceTime" in alarm_result["targetAttrs"]:
            face_time = alarm_result["targetAttrs"]["faceTime"]
            face_time = datetime.strptime(face_time, "%Y-%m-%dT%H:%M:%S%z")
            timestamp = int(face_time.timestamp())
            print("Got timestamp", timestamp)

        faces = alarm_result["faces"]
        # print('Got faces')
        for face in faces:
            # Get identify information
            if "identify" in face:
                identify = face["identify"][0]
                # print('Got identify')
                candidate = identify["candidate"][0]
                # print('Got candidate')
                reserve_field = candidate["reserve_field"]
                # print('Got reserve field')
                name = reserve_field["name"]
                # print('Got name')
                custom_pid = reserve_field["certificateNumber"]
                # camera_person_id = candidate["human_id"]
                # noti_logger.info(f"name: {name}, custom_pid: {custom_pid}")
                print(f"name: {name}, custom_pid: {custom_pid}")

                # Get image
                filename = f"temp/{name}_{timestamp}.jpg"
                with open(filename, "wb") as f:
                    f.write(image_data)

                image_url = minio_services.upload_file(
                    filename, filename.replace("temp/", "")
                )
                print("Uploaded image", image_url)
                # Remove the temporary image
                os.remove(filename)

                # Get person id from camera person id

                result = {
                    "image_url": image_url,
                    "user_id": custom_pid,
                    "timestamp": timestamp,
                    "ip_address": ip_address,
                }
                return result
        return None


hik_services = HIKServices()
