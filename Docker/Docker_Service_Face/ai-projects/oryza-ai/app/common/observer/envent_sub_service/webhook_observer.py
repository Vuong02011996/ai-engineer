from app.common.observer.envent_sub_service.observer_event import ObserverEvent
import requests
from app.common.constants.enums import AuthType
from app.services.webhook_services import webhook_services


def get_data(message: dict):
    from app.services import geo_unit_services

    data = message["data"]
    camera = message["camera"].model_dump()

    keys = ["name"]
    for key in keys:
        if key in camera:
            data[f"camera_{key}"] = camera[key]

    key_others = [
        "address",
        "coordinate",
        "id_vms",
        "coordinate_left",
        "coordinate_right",
    ]
    for key in key_others:
        if key in camera.get("other_info", {}):
            data[f"camera_{key}"] = camera["other_info"][key]

    if "camera_type" in camera.get("other_info", {}):
        data["camera_type"] = camera["other_info"]["camera_type"]

    if "ward_id" in camera:
        data["camera_address_path"] = geo_unit_services.get_address_full(
            camera["ward_id"]
        )
    # print("Data send webhook", data)
    return data


class WebhookObserver(ObserverEvent):
    def __init__(self, name):
        self._name = name

    def update(self, message):
        # print(f"{self._name} received message: {message}")
        try:
            webhooks = webhook_services.get_by_company_and_type_service(
                str(message["company"].id), str(message["type_service"].id)
            )
            for webhook in webhooks:
                if not webhook or webhook.status is False:
                    continue
                if webhook.auth_type == AuthType.header:
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": webhook.token,
                    }
                data = get_data(message)
                print(f"\nPush Webhook {webhook.name}: {data}\n")
                response = requests.post(webhook.endpoint, headers=headers, json=data)
                print(f"Push Webhook {webhook.name} result: ", response.text)
        except Exception as e:
            print("Error WebhookObserver: ", e)
