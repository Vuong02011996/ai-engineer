import requests

url = "http://192.168.103.25/RPC2_Loadfile/mnt/appdata1/userpic/SnapShot/2024-06-21/16/00/108_98_100_20240621160038364.jpg?timestamp=1718960855830"  # Thay thế bằng endpoint API thực tế của bạn
username = "your_username"
password = "your_password"

# Đăng nhập và lấy cookie
login_url = "http://example.com/login"  # Thay thế bằng URL đăng nhập thực tế của bạn
login_data = {"username": username, "password": password}

# Gửi yêu cầu POST để đăng nhập và lấy cookie
session = requests.Session()  # Tạo một phiên (session) để giữ cookie
login_response = session.post(login_url, data=login_data)

if login_response.status_code == 200:
    print("Login successful!")

    # Sau khi đăng nhập thành công, sử dụng session để gửi yêu cầu có chứa cookie
    response = session.get(url)

    if response.status_code == 200:
        print("Request successful!")
        print("Response:", response.text)
    else:
        print("Request failed with status code:", response.status_code)
else:
    print("Login failed with status code:", login_response.status_code)
