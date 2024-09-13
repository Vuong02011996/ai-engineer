import requests
from app.core.config import settings
from app.common.observer.envent_sub_service.observer_event import ObserverEvent
from app.services.vms_services import vms_services
from app.common.constants.rabbitmq_constants import (
    FACE_RECOGNITION_EXCHANGES,
    plate_number,
    crowd,
    DETECT_ITEMS_FORGOTTEN_EXCHANGES,
    IDENTIFY_UNIFORMS_EXCHANGES,
    loitering,
    tripwire,
    LINE_VIOLATION_EXCHANGES,
    LANE_VIOLATION_EXCHANGES,
    WRONG_WAY_EXCHANGES,
)


class VMSObserver(ObserverEvent):
    def __init__(self, name):
        self._name = name

    def push_vms(self, address: str, data: dict):
        url = f"{address}:{settings.VMS_PUSH_PORT}".replace("https", "http") + "/push"
        # print(f"\nPush VMS url: {url}")
        response = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
        )
        # print(f"\nPush VMS payload: {data}\n")
        if response.status_code != 200:
            print(f"Error pushing to VMS: {response.status_code} - {response.text}")
        else:
            print(f"Successfully push to VMS: {response.status_code} - {response.text}")

        url2 = "http://192.168.103.216:8080/push"
        response2 = requests.post(
            url2,
            json=data,
            headers={"Content-Type": "application/json"},
        )
        # print(f"\nPush VMS2 payload: {data}\n")
        if response2.status_code != 200:
            print(f"Error pushing to VMS2: {response2.status_code} - {response2.text}")
        else:
            print(
                f"Successfully push to VMS2: {response2.status_code} - {response2.text}"
            )

    def get_common_data(self, message: dict):
        """Get common data for all services: type_service, camera_id, camera_ip, timestamp, image_url"""
        return {
            "type_service": message["type_service"].key,
            "data": {
                "camera_id": f"{{{message['camera'].other_info['id_vms']}}}",
                "camera_ip": str(message["camera"].ip_address),
                "timestamp": int(message["data"]["timestamp"]) * 1000000,
            },
        }

    def get_face_recognition_data(self, message):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        data["data"]["name"] = message["data"]["name"]
        return data

    def get_plate_number_data(self, message):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["crop_plate"]
        data["data"]["license_plate"] = message["data"]["license_plate"]
        data["data"]["vehicle_type"] = message["data"]["vehicle_type"]
        data["data"]["vehicle_color"] = message["data"]["vehicle_color"]
        data["data"]["brand_name"] = message["data"]["brand_name"]
        return data

    def get_crowd_detection_data(self, message):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        data["data"]["total_people_detected"] = int(
            message["data"]["total_people_detected"]
        )
        data["data"]["crowd_members_count"] = int(
            message["data"]["crowd_members_count"]
        )
        return data

    def get_forget_items_data(self, message):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        return data

    def get_identify_uniforms_data(self, message):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        return data

    def get_loitering_detection_data(self, message: dict):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        return data

    def get_tripwire_data(self, message: dict):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        return data

    def get_lane_violation_data(self, message: dict):
        data = self.get_common_data(message)
        data["data"]["image_url"] = message["data"]["image_url"]
        return data

    def update(self, message: dict):
        # message = json.loads(message)
        # print(f"{self._name} received message: {message}")
        try:
            if not message["camera"].other_info:
                # print("Error SocketObserver: id_vms not found")
                return
            else:
                if (
                    "id_vms" not in message["camera"].other_info
                    or not message["camera"].other_info["id_vms"]
                ):
                    print("Error VMSObserver: id_vms not found")
                    return
            type_service_key = message["type_service"].key
            if type_service_key == FACE_RECOGNITION_EXCHANGES:
                data = self.get_face_recognition_data(message)
            elif type_service_key == plate_number:
                data = self.get_plate_number_data(message)
            elif type_service_key == crowd:
                data = self.get_crowd_detection_data(message)
            elif type_service_key == DETECT_ITEMS_FORGOTTEN_EXCHANGES:
                data = self.get_forget_items_data(message)
            elif type_service_key == IDENTIFY_UNIFORMS_EXCHANGES:
                data = self.get_identify_uniforms_data(message)
            elif type_service_key == loitering:
                data = self.get_loitering_detection_data(message)
            elif type_service_key == tripwire:
                data = self.get_tripwire_data(message)
            elif type_service_key in [
                LINE_VIOLATION_EXCHANGES,
                LANE_VIOLATION_EXCHANGES,
                WRONG_WAY_EXCHANGES,
            ]:
                data = self.get_lane_violation_data(message)
                data["data"]["image_url"] = message["data"]["image_url"]

            vms = vms_services.get_by_company_id(company_id=str(message["company"].id))
            self.push_vms(vms.ip_address, data)
        except Exception as e:
            print("Error VMSObserver: ", e)
