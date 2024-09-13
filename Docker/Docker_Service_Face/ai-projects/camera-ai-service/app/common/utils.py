import re
import random
import logging
from datetime import datetime, timedelta
import socket
import requests
from fastapi import HTTPException
from app.core.config import settings
from enum import Enum
from requests.auth import HTTPDigestAuth
from typing import Optional


class RequestType(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipV4 = s.getsockname()[0]
    s.close()
    return ipV4


this_server_ip = get_ipv4_address()


def text_to_object(data_response_text):
    data_dict = {}

    # Use regular expression to extract key-value pairs and populate the dictionary
    pattern = r"(\w+)\[(\d+)\]\.(\w+)(?:\[(\d+)\])?=(.*)\r\n"
    matches = re.findall(pattern, data_response_text)
    for group, group_index, key, key_index, value in matches:
        if key_index:
            key_index = int(key_index)
            data_dict.setdefault(group, {})
            data_dict[group].setdefault(int(group_index), {})
            data_dict[group][int(group_index)].setdefault(key, {})
            data_dict[group][int(group_index)][key][key_index] = value
        else:
            data_dict.setdefault(group, {})
            data_dict[group].setdefault(int(group_index), {})
            data_dict[group][int(group_index)][key] = value

    return data_dict


def clean_update_input(obj_in):
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    # Exclude empty fields
    update_data = {k: v for k, v in update_data.items() if v is not None and v != ""}
    return update_data


def get_times_around_event(event_time, delta_seconds=5):
    before_time = event_time - timedelta(seconds=delta_seconds)
    after_time = event_time + timedelta(seconds=int(delta_seconds / 2))
    return before_time, after_time


def request_subserver(
    request_type: str,
    url: str,
    payload: Optional[dict] = None,
    files: Optional[list] = None,
    timeout: int = settings.REQUEST_TIMEOUT,
    auth: Optional[HTTPDigestAuth] = None,
):
    if request_type not in RequestType.__members__:
        raise ValueError("Request type is not valid")
    try:
        response = requests.request(
            request_type,
            url,
            files=files,
            data=payload if files else None,
            json=None if files else payload,
            timeout=timeout,
            auth=auth,
        )
    except requests.exceptions.Timeout:
        print("Request timeout")
        raise HTTPException(status_code=408, detail="Request timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request subserver error: {e}")
        raise HTTPException(status_code=500, detail="Request subserver error")

    code = response.status_code
    if code != 200 and code != 201:
        print("Response: ", response.text)
        raise HTTPException(status_code=code, detail=response.text)

    if response.text:
        return response.json()
    else:
        return None


def generate_nonce():
    return "{:x}".format(random.getrandbits(160))


def generate_nc():
    return "{:08x}".format(random.randint(0, 0xFFFFFFFF))


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid adding handlers if they are already there
        handler = logging.StreamHandler()  # Console handler
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevents propagation to the root logger
    return logger


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


# For testing
if __name__ == "__main__":
    event_time_str = "2024-05-02 12:34:25"
    before_time_str, after_time_str = get_times_around_event(event_time_str)
    print(f"Before: {before_time_str}, After: {after_time_str}")
