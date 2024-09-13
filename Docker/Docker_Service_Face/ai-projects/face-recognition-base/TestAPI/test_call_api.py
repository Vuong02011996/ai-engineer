import requests
import json


def test_api():
    url = "http://192.168.111.98:30000/api/identities/register"

    payload = json.dumps({
      "name": "Vuong",
      "user_id": "64b76ab4-ec05-44c2-9349-35bfe3b5f55c",
      "type": "Nhan vien",
      "data": [
        "/home/oryza/Pictures/Face/Vuong.jpeg"
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    test_api()