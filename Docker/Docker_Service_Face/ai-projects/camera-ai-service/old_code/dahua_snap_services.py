# NOT BE USED ANYMORE
import requests
import hashlib
from urllib.parse import urlparse
import uuid
import logging

from app.common.utils import generate_nonce, generate_nc, get_past_datetime
from app.services.minio_services import MinioServices


SNAP_LOGGER = logging.getLogger("dahua_snap")


def get_snap(url, method, username, password, image_file_name):
    try:
        session = requests.Session()
        response = session.get(url)
        auth_params = requests.utils.parse_dict_header(
            response.headers["WWW-Authenticate"]
        )
        realm = auth_params["Digest realm"]
        nonce = auth_params["nonce"]
        qop = auth_params["qop"]
        opaque = auth_params.get("opaque", "")
        nc = generate_nc()
        cnonce = generate_nonce()
        uri = urlparse(url).path
        ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode("utf-8")).hexdigest()
        ha2 = hashlib.md5(f"{method}:{uri}".encode("utf-8")).hexdigest()
        response_hash = hashlib.md5(
            f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode("utf-8")
        ).hexdigest()

        auth_header = (
            f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", '
            f'response="{response_hash}", qop="{qop}", opaque="{opaque}", '
            f'nc={nc}, cnonce="{cnonce}"'
        )

        req_headers = {"Authorization": auth_header}

        response = session.get(url, headers=req_headers)

        # Check the response
        if response.status_code == 200:
            # SNAP_LOGGER.info("Authentication successful.")
            with open(image_file_name, "wb") as f:
                f.write(response.content)
            # SNAP_LOGGER.info("Image downloaded.")
        # else:
        # print(f"Authentication failed. Status code: {response.status_code}")
        # print(response)
        return response

    except requests.exceptions.RequestException as e:
        SNAP_LOGGER.debug(f"Error occurred: {e}")


class DahuaSnapServices:
    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.method = "GET"
        self.username = username
        self.password = password
        self.upload_services = MinioServices()

    def get_image_url(self, event_date, event_time):
        """
        Example:
            snap_date = "2021-08-31"
            snap_time = "08:31:26"
        """
        # Try the time
        try_seconds = [0, 1, -1, 2, -2]
        image_indices = [2, 1]
        image_url = None

        for try_second in try_seconds:
            for image_index in image_indices:
                snap_date, snap_time = get_past_datetime(
                    event_date, event_time, try_second
                )
                request_url = f"http://{self.server}/cgi-bin/RPC_Loadfile/mnt/sd/{snap_date}/001/jpg/{snap_time}[M][0@0][{image_index}].jpg"
                SNAP_LOGGER.debug(f"Trying {request_url}")
                shortuuid = uuid.uuid4().hex[:6]
                temp_image_file_name = (
                    f"./temp/{snap_date}_{snap_time.replace('/', '-')}_{shortuuid}.jpg"
                )
                response = get_snap(
                    request_url,
                    self.method,
                    self.username,
                    self.password,
                    temp_image_file_name,
                )
                if response is None:
                    # logging.error("No response received from get_snap")
                    continue
                if response.status_code == 200:
                    SNAP_LOGGER.info(f"Image downloaded from {request_url}")
                    try:
                        image_url = self.upload_services.upload_file(
                            temp_image_file_name, temp_image_file_name.split("/")[-1]
                        )
                        SNAP_LOGGER.info(f"Image uploaded. URL: {image_url}")
                        # os.remove(temp_image_file_name)  # TODO: Uncomment this line
                    except Exception as e:
                        SNAP_LOGGER.error(e)
                    break
            if image_url:
                break

        if image_url:
            return image_url
        else:
            return False
