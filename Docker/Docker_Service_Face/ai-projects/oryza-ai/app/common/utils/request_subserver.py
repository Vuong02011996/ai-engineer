import requests
from fastapi import HTTPException

from app.common.constants.enums import RequestType
from app.core.config import settings


def request_subserver(
    request_type: str,
    url: str,
    payload: dict,
    files: list = None,
    timeout: int = settings.REQUEST_TIMEOUT,
):
    if request_type not in RequestType.__members__:
        raise ValueError("Request type is not valid")
    try:
        if files:
            response = requests.request(
                request_type, url, files=files, data=payload, timeout=timeout
            )
        else:
            response = requests.request(
                request_type, url, json=payload, timeout=timeout
            )
    except requests.exceptions.Timeout:
        print("Request timeout")
        raise HTTPException(status_code=408, detail="Request timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request subserver error: {e}")
        raise HTTPException(status_code=500, detail="Request subserver error")

    code = response.status_code
    if code != 200 and code != 201:
        print("Response: ", response.json())
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()
