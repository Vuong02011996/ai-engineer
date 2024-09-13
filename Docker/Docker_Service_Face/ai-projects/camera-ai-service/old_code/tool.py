import shutil
import time

import psutil
import os


def get_info_drive():
    # Kiểm tra nếu đang chạy trong môi trường tệp .py hoặc môi trường tương tác
    try:
        # Lấy đường dẫn tuyệt đối của tệp đang chạy
        current_file_path = os.path.abspath(__file__)
    except NameError:
        # Nếu __file__ không tồn tại (trong môi trường tương tác)
        current_file_path = os.getcwd()
    # Lấy ổ đĩa chứa tệp đang chạy hoặc thư mục hiện tại
    current_drive = os.path.splitdrive(current_file_path)[0]
    if not current_drive:
        # Trường hợp không phải Windows (Unix-like)
        current_drive = "/"
    # Lấy thông tin về dung lượng của ổ đĩa chứa tệp đang chạy
    partition_usage = psutil.disk_usage(current_drive)

    # Tổng dung lượng và dung lượng trống
    total_storage = partition_usage.total
    total_free = partition_usage.free

    # Đổi đơn vị từ byte sang gigabyte
    total_storage_gb = total_storage / (1024**3)
    total_free_gb = total_free / (1024**3)

    # Tính phần trăm dung lượng trống
    percent_free = (total_free / total_storage) * 100

    return current_drive, total_storage_gb, total_free_gb, percent_free


# print(f"Ổ đĩa chứa tệp hoặc thư mục hiện tại: {current_drive}")
# print(f"Tổng dung lượng lưu trữ: {total_storage_gb:.2f} GB")
# print(f"Dung lượng lưu trữ trống: {total_free_gb:.2f} GB")
# print(f"Phần trăm dung lượng trống: {percent_free:.2f}%")
# print(f"Phần trăm dung lượng đã sử dụng: {100 - percent_free:.2f}%")

list_url = ["/home/linh/Downloads/demo", "/home/linh/Downloads/demo2"]
while True:
    current_drive, total_storage_gb, total_free_gb, percent_free = get_info_drive()
    # print(f"Ổ đĩa chứa tệp hoặc thư mục hiện tại: {current_drive}")
    # print(f"Tổng dung lượng lưu trữ: {total_storage_gb:.2f} GB")
    print(f"Dung lượng lưu trữ trống: {total_free_gb:.2f} GB")
    # print(f"Phần trăm dung lượng đã sử dụng: {100 - percent_free:.2f}%")
    if percent_free < 15:
        for i in list_url:
            list_folder = os.listdir(i)
            list_folder.sort()
            # print(list_folder)
            if len(list_folder) > 0:
                first_folder = list_folder[0]
                # delete folder
                shutil.rmtree(i + "/" + first_folder)

    time.sleep(60)
