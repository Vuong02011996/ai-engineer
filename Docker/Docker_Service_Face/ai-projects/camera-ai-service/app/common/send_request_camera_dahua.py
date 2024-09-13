import requests
import random

# Generate the response hash
import hashlib
from urllib.parse import urlparse
import re


def text_to_object(data_response_text):
    data_dict = {}

    # Use regular expression to extract key-value pairs and populate the dictionary
    pattern = r"(\w+)\[(\d+)\]\.(\w+)(?:\[(\d+)\])?=(.*)"
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


def generate_nonce():
    return "{:x}".format(random.getrandbits(160))


def generate_nc():
    return "{:08x}".format(random.randint(0, 0xFFFFFFFF))


def perform_digest_authentication(url, method, username, password, image=None):
    try:
        # Create a session object
        session = requests.Session()

        # Make an initial request to get the authentication parameters
        response = session.get(url)

        # Parse the authentication parameters from the response
        auth_params = requests.utils.parse_dict_header(
            response.headers["WWW-Authenticate"]
        )

        # Prepare the necessary data for digest authentication
        realm = auth_params["Digest realm"]
        nonce = auth_params["nonce"]
        qop = auth_params["qop"]
        opaque = auth_params.get("opaque", "")

        # Generate the nonce count (nc)
        nc = generate_nc()

        # Generate the client nonce (cnonce)
        cnonce = generate_nonce()

        uri = urlparse(url).path
        ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode("utf-8")).hexdigest()
        ha2 = hashlib.md5(f"{method}:{uri}".encode("utf-8")).hexdigest()
        response_hash = hashlib.md5(
            f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode("utf-8")
        ).hexdigest()

        # Prepare the Authorization header
        auth_header = (
            f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{uri}", '
            f'response="{response_hash}", qop="{qop}", opaque="{opaque}", '
            f'nc={nc}, cnonce="{cnonce}"'
        )

        req_headers = {"Authorization": auth_header}
        if image:
            req_headers["Content-Type"] = "image/jpeg"

        # Make a new request with the Authorization header for Digest authentication
        if method == "GET":
            # from requests_toolbelt.multipart.decoder import MultipartDecoder

            response = session.get(url, headers=req_headers)
            # if "faceRecognitionServer.cgi?action=startFind&condition.GroupID[0]" not in url:
            # try:
            #     if response.status_code == 200:
            #         content_type = response.headers.get('Content-Type', '')
            #         if 'multipart/x-mixed-replace' in content_type:
            #             boundary = content_type.split('boundary=')[-1].strip('"')
            #
            #             buffer = b''
            #             for chunk in response.iter_content(chunk_size=1024):
            #                 buffer += chunk
            #                 while True:
            #                     part_index = buffer.find(boundary.encode())
            #                     if part_index == -1:
            #                         break
            #                     part = buffer[:part_index]
            #                     buffer = buffer[part_index + len(boundary):]
            #
            #                     if part:
            #                         headers_end = part.find(b'\r\n\r\n')
            #                         if headers_end != -1:
            #                             headers = part[:headers_end].decode('utf-8')
            #                             body = part[headers_end + 4:]
            #
            #                             if 'Content-Type: text/plain' in headers:
            #                                 text_data = body.decode('utf-8')
            #                                 print("Text Data:")
            #                                 print(text_data)
            #                             elif 'Content-Type: image/jpeg' in headers:
            #                                 with open('image.jpg', 'wb') as f:
            #                                     f.write(body)
            #                                 print("Image data saved as image.jpg")
            #
            #                             # Break if you want to stop after one part
            #                             # break
            #     else:
            #         print(f"Failed to connect, status code: {response.status_code}")
            # except Exception as e:
            #     print(e)

        elif method == "POST":
            # print(req_headers)
            response = session.post(url, headers=req_headers, data=image)

        # Check the response
        if response.status_code == 200:
            # return json
            return response.text
        else:
            raise Exception(
                f"Authentication failed. Status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        raise Exception(e)


if __name__ == "__main__":
    url = "http://192.168.103.24/cgi-bin/RPC_Loadfile/mnt/appdata1/userpic/SnapShot/2024-06-14/17/34/3_90_100_20240614173419214.jpg"
    url = "http://192.168.103.25/8/cgi-bin/FileManager.cgi?action=downloadFile&fileName=/mnt/appdata1/userpic/SnapShot/2024-06-21/16/00/108_98_100_20240621160038364.jpg"
    username = "admin"
    password = "admin123"
    method = "GET"
    image = None
    print(perform_digest_authentication(url, method, username, password, image))
