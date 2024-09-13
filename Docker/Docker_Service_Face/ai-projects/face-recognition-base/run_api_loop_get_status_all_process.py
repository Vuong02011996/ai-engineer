import requests
import time


# ip_run_service_ai = "192.168.111.98"
ip_run_service_ai = "192.168.103.81"
url = "http://" + ip_run_service_ai + ":30000/get_status_all_process"

while True:
    payload = ""
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        if response.json()['status_code'] == 200:
            break
    except Exception as e:
        print(e)
        time.sleep(10)
        continue
