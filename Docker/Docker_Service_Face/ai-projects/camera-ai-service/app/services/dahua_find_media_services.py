import requests
import hashlib
import logging
import os
import uuid
from urllib.parse import urlparse, quote
from datetime import datetime

from app.common.utils import generate_nonce, generate_nc
from app.services.minio_services import MinioServices

logger = logging.getLogger("media_finder_logger")


def get_authentication_header(url, method, username, password):
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

        return {"Authorization": auth_header}
    except requests.exceptions.RequestException as e:
        logger.debug(f"Error occurred: {e}")


class DahuaFindMediaService:
    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.method = "GET"
        self.username = username
        self.password = password
        self.upload_services = MinioServices()

    def get_image_url(self, condition: dict):
        """
        Ref: DAHUA_HTTP_API_V3, page 187, 4.10.5 Find Media Files -> 4.10.7 Find Media By Recognition info
        """
        print("ID:", id)
        # Step 1: Create a media finder
        url = f"http://{self.server}/cgi-bin/mediaFileFind.cgi?action=factory.create"
        header = get_authentication_header(
            url, self.method, self.username, self.password
        )
        response = requests.get(url, headers=header)
        if response.status_code != 200 or "error" in response.content.decode().strip():
            return None, None
        finder_id = response.content.decode().split("=")[1].strip()
        logger.info(f"Create media result: Finder ID: {finder_id}")

        # Step 2: Find media
        condition_params = []
        for key, value in condition.items():
            if isinstance(value, list):
                for i, v in enumerate(value):
                    condition_params.append(
                        f"condition.{quote(key)}[{i}]={quote(str(v))}"
                    )
            else:
                condition_params.append(f"condition.{quote(key)}={quote(str(value))}")
        url = (
            f"http://{self.server}/cgi-bin/mediaFileFind.cgi?action=findFile&object={finder_id}"
            f"&{'&'.join(condition_params)}"
        )
        header = get_authentication_header(
            url, self.method, self.username, self.password
        )
        url = url + (
            f"&condition.DB.FaceRecognitionRecordFilter.RegType=RecSuccess"
            f"&condition.DB.FaceRecognitionRecordFilter.StartTime={quote(condition['StartTime'])}"
            f"&condition.DB.FaceRecognitionRecordFilter.EndTime={quote(condition['EndTime'])}"
            f"&condition.DB.FaceRecognitionRecordFilter.CertificateType={condition['certificate_type']}"
            f"&condition.DB.FaceRecognitionRecordFilter.Person.ID={condition['ID']}"
        )
        response = requests.get(url, headers=header)
        logger.info(
            f"Find media: Code:{response.status_code}, Msg: {response.content.decode().strip()}"
        )
        if response.status_code != 200 or "error" in response.content.decode().strip():
            return None, None

        # Step 3: Get media
        url = f"http://{self.server}/cgi-bin/mediaFileFind.cgi?action=findNextFile&object={finder_id}&count=1"
        header = get_authentication_header(
            url, self.method, self.username, self.password
        )
        response = requests.get(url, headers=header)
        lines = response.content.decode().split("\n")
        file_path = ""
        for line in lines:
            if line.startswith("items[0].SummaryNew[0].Value.Object.Image.FilePath="):
                file_path = line.split("=")[1].strip()[1:]
            elif line.startswith("items[0].SummaryNew[0].Value.Object.SnapTime="):
                timestamp = line.split("=")[1].strip()
                logger.info(
                    f"Get media result: File Path: {file_path}, timestamp: {timestamp}"
                )
                break
        if file_path == "":
            return None, None

        # Download media
        url = f"http://{self.server}/cgi-bin/RPC_Loadfile/{file_path}"
        header = get_authentication_header(
            url, self.method, self.username, self.password
        )
        response = requests.get(url, headers=header)
        timestamp = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")
        timestamp_str = datetime.strftime(timestamp, "%Y-%m-%d_%H-%M-%S")

        destination_file = (
            timestamp_str  # Use the formatted timestamp
            + "_"
            + str(uuid.uuid4())[:8]  # Add a short UUID
            + ".jpg"
        )
        source_file = f"./temp/{destination_file}"

        logger.info(f"Download media result: Code: {response.status_code})")
        with open(source_file, "wb") as f:
            f.write(response.content)

        # Step 4: Upload media and get image URL
        image_url = self.upload_services.upload_file(
            source_file=source_file, destionation_file=destination_file
        )
        logger.info(f"Upload media result: Image URL: {image_url}")
        # Remove file in temp
        os.remove(source_file)

        # Step 5: Close the finder
        url = f"http://{self.server}/cgi-bin/mediaFileFind.cgi?action=close&object={finder_id}"
        header = get_authentication_header(
            url, self.method, self.username, self.password
        )
        response = requests.get(url, headers=header)
        logger.info(
            f"Close finder result: Code: {response.status_code}, Msg: {response.content.decode().strip()}"
        )
        return timestamp, image_url


if __name__ == "__main__":
    media_finder = DahuaFindMediaService(
        server="192.168.111.6", username="admin", password="Oryza@123"
    )
    uid = "2"
    condition = {
        "Channel": 1,
        "StartTime": "2024-05-24 08:02:27",
        "EndTime": "2024-05-24 08:12:38",
        "Types": ["jpg"],
        "Flags": ["Event"],
        "Events": ["FaceRecognition"],
    }
    timestamp, image_url = media_finder.get_image_url(uid=uid, condition=condition)
    print(image_url)
    print(timestamp)
