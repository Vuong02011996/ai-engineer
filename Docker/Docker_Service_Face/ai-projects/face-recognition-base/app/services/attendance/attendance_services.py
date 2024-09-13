import re
import time

import numpy as np
import multiprocessing as mp
import signal
import os
import cv2
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from flask import Blueprint, request
from flask_restx import Api, Resource
from bson import ObjectId
import sys

from app.app_utils.file_io_untils import upload_img_from_disk
from app.services.services_helper import pagination, update_status_job, get_utc_time_from_datetime, \
    get_frame_url_from_cam, get_token_login
from app.services.attendance.attendance_helper import get_object_info_roll_call, get_object_roll_call_date, \
    get_object_roll_call_name
from app.mongo_dal.camera_dal import CameraDAL
from app.mongo_dal.identity_dal import IdentityDAL
from app.mongo_dal.object_dal.object_attendance_dal import ObjectAttendanceDAL
from app.mongo_dal.process_dal.process_attendance_dal import ProcessAttendanceDAL
from app.services.attendance.attendance_model import run_roll_call

blueprint = Blueprint("Attendance", __name__)
ns = Api(blueprint)
namespace = ns.namespace("Attendance")

# Sử dụng để viết api bất đồng bộ
executor = ThreadPoolExecutor(2)

camera_dal = CameraDAL()
object_dal = ObjectAttendanceDAL()
process_dal = ProcessAttendanceDAL()
identity_dal = IdentityDAL()
start_server = True
url_report_attendance_teacher = os.getenv("url_report_attendance_teacher")


"""
# Nếu mới start server thì mọi status_process điểm danh đều phải Stop,
# Mỗi lần start lại camera lại load file env chạy lại toàn bộ server. Do dùng multiprocess
# Nên không stop all process chỗ này được.
"""


# list_all_item_process = process_dal.find_all_item()
# for process in list_all_item_process:
#     if process["status_process"] != "Stop":
#         data_update = {
#             "status_process": "Stop",
#         }
#         process_dal.update({"_id": process["_id"]}, data_update)
#
# list_all_item_camera = camera_dal.find_all_item()
# for camera in list_all_item_camera:
#     if camera.get("jobs_cam") is not None \
#         and camera["jobs_cam"].get("roll_call") is not None \
#         and camera["jobs_cam"]["roll_call"].get("status_process") is not None \
#         and camera["jobs_cam"]["roll_call"]["status_process"] == "RUNNING":
#         # Giữ toàn bộ config cũ
#         jobs_cam_update = camera["jobs_cam"]
#         # Update data status mới
#         jobs_cam_update["roll_call"]["status_process"] = "NOT_RUN"
#         data_update = {
#             "jobs_cam": jobs_cam_update,
#             "created_at": datetime.now(),
#         }
#         camera_dal.update({"_id": camera["_id"]}, data_update)


@namespace.route("/update_config/<_id>", methods=["GET", "PUT", "DELETE"])
class FindById(Resource):
    def put(self, _id):
        """
        Update info a new camera
        Example: Put json
        {
            "jobs_cam": {
                    "roll_call": {
                        "coordinates": [[0.36, 0.34], [0.67, 0.39], [0.71, 0.86], [0.32, 0.91]],
                        "from_time": "y-m-d H:i:s",("2021-12-01 01:01:14")
                        "to_time": "y-m-d H:i:s"
                    }
        }
        :param _id:  mongo id camera Ex http://14.241.120.239:8001/clover/test/v2.0/api/cameras/update/618a4408a71ca0ac64b1df02
        :return:
        {
            "status": true,
            "status_code": 200,
            "message": "Update a camera successfully!"
        }
        """
        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options
        jobs_cam_update_new = request_data.get("jobs_cam")
        print("jobs_cam_update_new: ", jobs_cam_update_new)
        mongo_id = ObjectId(_id)
        item_cam = camera_dal.find_by_id(_id)
        if item_cam.get("jobs_cam") is not None:
            jobs_cam_update = item_cam["jobs_cam"]
            if jobs_cam_update.get("roll_call") is None:
                jobs_cam_update["roll_call"] = {}
        else:
            jobs_cam_update = {"roll_call": {}}

        if jobs_cam_update_new is not None:
            if jobs_cam_update_new.get("roll_call") is not None:
                if jobs_cam_update_new['roll_call'].get("coordinates") is not None:
                    jobs_cam_update["roll_call"]["coordinates"] = jobs_cam_update_new["roll_call"]["coordinates"]
                if jobs_cam_update_new['roll_call'].get("from_time") is not None:
                    jobs_cam_update["roll_call"]["from_time"] = jobs_cam_update_new["roll_call"]["from_time"]
                if jobs_cam_update_new['roll_call'].get("to_time") is not None:
                    jobs_cam_update["roll_call"]["to_time"] = jobs_cam_update_new["roll_call"]["to_time"]
                if jobs_cam_update_new['roll_call'].get("process_name") is not None:
                    jobs_cam_update["roll_call"]["process_name"] = jobs_cam_update_new["roll_call"]["process_name"]
                if jobs_cam_update_new['roll_call'].get("status_process") is not None:
                    jobs_cam_update["roll_call"]["status_process"] = jobs_cam_update_new["roll_call"]["status_process"]

        data_update = {
            "jobs_cam": jobs_cam_update,
            "created_at": datetime.now(),
        }

        camera_dal.update({"_id": mongo_id}, data_update)
        options = {"status": True, "status_code": 200, "message": "Update a camera successfully!"}

        return options


@namespace.route("/get_current_config/<_id>", methods=["GET"])
class FindById(Resource):
    """
    _id: _id camera
      "roll_call": {
                    "coordinates": [[0.36, 0.34], [0.67, 0.39], [0.71, 0.86], [0.32, 0.91]],
                    "from_time": "y-m-d H:i:s",("2021-12-01 01:01:14")
                    "to_time": "y-m-d H:i:s"
                }
    """

    def get(self, _id):
        # # mongo_id = camera_dal.find_one_by_condition({"name_cam": name_cam}, columns={"_id": 1})
        # mongo_id = ObjectId(_id)
        item_cam = camera_dal.find_by_id(_id)
        #  Chỗ này cần lấy thêm frame ảnh của camera và update vào frame_url của db
        #  Sau đó cũng gửi frame_url này đến api get current config, để FE lấy thông tin frame_url để khi
        #  bấm vào nút vẽ vùng sẽ hiển thị frame url này lên modal và vẽ...
        # ban đầu sẽ lấy frame_url từ cam sau đó , nếu quá cũ hơn một ngày thì thì lấy cái ảnh mới

        match = re.search(r'\d{8}', item_cam['frame_url'])
        if match:
            date_str = match.group()
            print(date_str)
            date = datetime.strptime(date_str, '%Y%m%d')
            timestamp = date.timestamp()
            current_timestamp = time.time()
            # Tính khoảng cách giữa hai epoch time tính bằng giây
            time_diff = current_timestamp - timestamp
            # Kiểm tra xem khoảng cách này có lớn hơn 7 ngày hay không
            one_day_in_seconds = 24 * 60 * 60 * 7
            if time_diff < one_day_in_seconds:
                print("Lấy  frame_url từ DB")
                frame_url = item_cam["frame_url"]
            else:
                frame_url = get_frame_url_from_cam(item_cam['url_cam'])
                data_update = {
                    "frame_url": frame_url,
                    "created_at": datetime.now(),
                }
                # Update frame_url vào DB
                camera_dal.update({"_id": item_cam["_id"]}, data_update)
                print("Tạo  frame_url mới")
        else:
            print('Không tìm thấy ngày trong url')
            frame_url = get_frame_url_from_cam(item_cam['url_cam'])
            data_update = {
                "frame_url": frame_url,
                "created_at": datetime.now(),
            }
            # Update frame_url vào DB
            camera_dal.update({"_id": item_cam["_id"]}, data_update)
            print("Tạo  frame_url mới")

        if item_cam.get("jobs_cam") is not None and item_cam.get("jobs_cam").get("roll_call") is not None:
            data = item_cam["jobs_cam"]["roll_call"]
            data["frame_url"] = frame_url
            options = {"status": True, "status_code": 200, "message": "Update a camera successfully!", "data": data}
            return options
        else:
            options = {"status": True, "status_code": 200, "message": "Info cam haven't jobs_cam or roll_call!",
                       "data": {}}
            return options


@namespace.route("/start/<_id>", methods=["GET"])
class StartById(Resource):
    def get(self, _id):
        """
        :param _id: id camera
        :return:
        """
        # check if start server all process is running must stop, if stop incorrect
        # Trường hợp mới start server thì tất cả process phải stop(sửa lỗi trường hợp process không được stop đúng cách)
        list_all_item_process = process_dal.find_all_item()
        global start_server
        if start_server:
            for process in list_all_item_process:
                if process["status_process"] != "Stop":
                    data_update = {
                        "status_process": "Stop",
                    }
                    process_dal.update({"_id": process["_id"]}, data_update)
            start_server = False

        #  Kiểm tra nếu cam id đang chạy điểm danh thì return
        list_all_item_process = process_dal.find_all_item()
        for p in list_all_item_process:
            if p["process_name"].split("_")[0] == _id and p["status_process"] == "running" and (
                    "roll_call" in p["process_name"]):
                print("Camera is running roll call, process_name is {}".format(p["process_name"]))
                options = {"status": False, "status_code": 500, "message": "Camera đang chạy điểm danh!"}
                return options

        camera_id = ObjectId(_id)
        item_cam = camera_dal.find_by_id(camera_id)

        # Check camera đã lưu cấu hình nhiệm vụ hay chưa.
        if item_cam.get("jobs_cam") is None or item_cam["jobs_cam"].get("roll_call") is None:
            print("Cam cannot start, Camera chưa cấu hình vùng điểm danh")
            options = {"status": False, "status_code": 500, "message": "Camera chưa cấu hình vùng điểm danh"}
            return options

        # Get from time and end time to start and kill process
        time_utc_now = datetime.utcnow()
        time_now = datetime.now()
        time_now_seconds = time_utc_now.timestamp()

        format_time = "%Y-%m-%dT%H:%M:%S.%fZ"
        from_time = item_cam["jobs_cam"]["roll_call"]["from_time"]
        end_time = item_cam["jobs_cam"]["roll_call"]["to_time"]
        from_time_str = time_utc_now.strftime("%Y-%m-%d") + "T" + from_time.split("T")[-1]
        end_time_str = time_utc_now.strftime("%Y-%m-%d") + "T" + end_time.split("T")[-1]
        # Convert string time to datetime
        from_time_dt = datetime.strptime(from_time_str, format_time)
        end_time_dt = datetime.strptime(end_time_str, format_time)
        from_time_s = from_time_dt.timestamp()
        end_time_s = end_time_dt.timestamp()

        print("time_now_seconds: ", time_now_seconds)
        print("from_time_s: ", from_time_s)
        print("end_time_s: ", end_time_s)

        # if time_now_seconds > end_time_s or time_now_seconds < from_time_s:
        #     print("Cam cannot start, Thời gian hiện tại nằm ngoài thời điểm để điểm danh!")
        #     options = {"status": False, "status_code": 500,
        #                "message": "Thời gian hiện tại nằm ngoài thời điểm để điểm danh"}
        #     return options

        # Create new process
        process_name = _id + "_roll_call_" + str(len(process_dal.find_all_item())) + "_" + \
                       time_now.strftime("%Y:%m:%d-%H:%M:%S")

        # Delete all objects if process name có tồn tại trong db
        process_id = process_dal.find_object_id_by_process_name(process_name)
        if len(process_id) > 0:
            for i in range(len(process_id)):
                process_dal.delete({"_id": process_id[i]["_id"]})

        try:
            def process_data():
                print("Đang xử lý logic bên trong API...")
                # Using multiprocess
                # RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing,
                # you must use the 'spawn' start method
                # global start_server
                # if start_server:
                #     # Chỉ set lần đầu tiên khi start server, nếu không khi start process lần 2 sẽ không
                #     # tạo process mới code không qua được dòng multiprocessing.set_start_method('spawn')
                #     print("Đang xử lý logic bên trong API start_server before mp.set_start_method('spawn')...", start_server)
                """
                Dòng code mp.set_start_method('spawn') phải để trước bất kì chỗ nào trong chương trình có dùng 
                multiprocessing.Process nếu dùng sau dòng multiprocessing.Process chương trình sẽ không chạy qua được dòng 
                mp.set_start_method('spawn')
                """
                #     mp.set_start_method('spawn')
                #     print("Đang xử lý logic bên trong API start_server...", start_server)
                #     start_server = False

                process = mp.Process(target=run_roll_call,
                                                  args=(item_cam, process_name, end_time_s, False))
                process.start()
                #  Create process data in mongoDB

                data_process = {
                    "process_name": process_name,
                    "multiprocessing_pid": process.pid,
                    "status_process": "running",
                    "camera": item_cam["_id"],
                    "created_at": datetime.now(),
                }
                process_dal.create_one(data_process)
                # Update status in jobcam roll call is RUNNING
                update_status_job(item_cam["_id"], item_cam, process_name, status_process="RUNNING", job="roll_call")
                print("Tạo process trên DB thành công...")

                process.join()
                process.terminate()
                # If process finished find process_id and change status to stop
                process_id = process_dal.find_object_id_by_process_name(process_name)
                data_update = {
                    "status_process": "Stop",
                    "created_at": datetime.now(),
                }
                if len(process_id) > 0:
                    process_dal.update({"_id": process_id[0]["_id"]}, data_update)
                    print("process_name {} Stop".format(process_name))

                # Update status in jobcam roll call is NOT_RUN
                update_status_job(item_cam["_id"], item_cam, process_name, status_process="NOT_RUN", job="roll_call")
                options = {"status": True, "status_code": 200, "process_name": process_name,
                           "status_process": "NOT_RUN",
                           "message": "Setup camera thành công! Bắt đầu chạy điểm danh"}
                return options

            executor.submit(process_data)
            options = {"status": True, "status_code": 200, "process_name": process_name,
                       "status_process": "RUNNING",
                       "message": "Setup camera thành công! Bắt đầu chạy điểm danh"}
            return options

        except RuntimeError:
            options = {"status": False, "status_code": 500, "process_name": process_name,
                       "status_process": "NOT_RUN",
                       "message": "Setup camera lỗi , chưa thể bắt đầu chạy điểm danh"}
            return options


@namespace.route("/stop/<process_name>", methods=["GET"])
class StopById(Resource):
    def get(self, process_name):
        """

        :param process_name:
        :return:
        """
        print("process_name: ", process_name)
        process_id = process_dal.find_object_id_by_process_name(process_name)
        if len(process_id) > 0:
            multiprocessing_pid = process_id[0]["multiprocessing_pid"]
            try:
                os.kill(multiprocessing_pid, signal.SIGTERM)
                print(f"multiprocessing_pid with PID {multiprocessing_pid} exists. Killed it")
            except ProcessLookupError:
                print(f"No multiprocessing_pid with PID {multiprocessing_pid}")

            data_update = {
                "status_process": "Stop",
                "created_at": datetime.now(),
            }
            process_dal.update({"_id": process_id[0]["_id"]}, data_update)
            print("process_name {} Stop".format(process_name))

        info_cam = process_dal.find_camera_by_process_name(process_name)
        if len(info_cam) == 0:
            options = {"status": True, "status_code": 200,
                       "process_name": process_name,
                       "status_process": "NOT_RUN",
                       "message": "Process name không tồn tại!"}

            return options

        item_cam = camera_dal.find_by_id(info_cam[0]["camera"])
        update_status_job(item_cam["_id"], item_cam, process_name, status_process="NOT_RUN", job="roll_call")
        options = {"status": True, "status_code": 200,
                   "process_name": process_name,
                   "status_process": "NOT_RUN",
                   "message": "Dừng điểm danh!"}

        return options


@namespace.route("/get_all_data", methods=["GET"])
class FindById(Resource):
    def get(self):
        """
        :param limit, page, branch_cam, class_cam
        :return: get all data from process _id + "_roll_call"
        Mongo Compass {process_name: "61d56d210d7c41e2668ec409_roll_call"}
        {process_name: "61d56d210d7c41e2668ec409_roll_call", have_new_face: true}
        Data format:
        """

        limit = request.args.get('limit', default=None, type=int)
        page = request.args.get('page', default=None, type=int)
        branch_id = request.args.get('branch_id', default=None, type=str)
        class_id = request.args.get('class_id', default=None, type=str)
        from_date = request.args.get('fromDate', default=None, type=str)
        to_date = request.args.get('toDate', default=None, type=str)
        user_id = request.args.get('user_id', default=None, type=str)

        if user_id is not None and len(user_id) > 0:
            list_user_id_search = user_id.split(",")
        else:
            list_user_id_search = None

        item = object_dal.find_all_item()

        # Filter item item["have_new_face"] is True and sort time.
        new_item = []
        list_time = []
        for i in range(len(item)):
            hs = item[i]
            date_time = hs["created_at"]
            seconds = date_time.timestamp()
            if hs["have_new_face"] is True:
                # only filter hs was had recognition
                # if list_user_id_search is not None:
                if hs.get("identity_name") is not None:
                    new_item.append(item[i])
                    list_time.append(seconds)
            # else:    # take all hs have face
            #     new_item.append(item[i])
            #     list_time.append(seconds)
        list_index_sort = np.argsort(np.array(list_time))[::-1]
        item = np.array(new_item)[list_index_sort]

        if from_date is not None and to_date is not None:
            new_item = []
            for i in range(len(item)):
                hs = item[i]
                date_time = hs["created_at"]
                seconds = date_time.timestamp()
                from_date_second = datetime.strptime(from_date, "%Y-%m-%d").timestamp()
                to_date_second = datetime.strptime(to_date, "%Y-%m-%d").timestamp()
                if seconds < to_date_second + 86400 and (seconds > from_date_second):
                    new_item.append(hs)
            item = new_item
        if class_id is not None:
            # find id camera by branch_id
            id_cam = camera_dal.find_id_by_class_id(class_id=class_id)
            if len(id_cam) == 0:
                options = {"message": "class_id found any camera"}
                return options

            id_cam = str(id_cam[0]["_id"])
            process_name = id_cam + "_roll_call"
            new_item = []
            for i in range(len(item)):
                if process_name in item[i]["process_name"]:
                    new_item.append(item[i])
            item = new_item

        if branch_id is not None:
            # find id camera by branch_id
            new_item = []
            id_cam = camera_dal.find_id_by_branch_id(branch_id=branch_id)
            if len(id_cam) == 0:
                options = {"message": "branch_id found any camera"}
                return options

            id_cam = str(id_cam[0]["_id"])

            process_name = id_cam + "_roll_call"
            for i in range(len(item)):
                if process_name in item[i]["process_name"]:
                    new_item.append(item[i])
            item = new_item

        new_item = []
        list_name_remain = []

        for hs in item:
            object_info = get_object_info_roll_call(hs, list_name_remain, list_user_id_search)
            if object_info is not None:
                new_item.append(object_info)

        data_out = pagination(limit, new_item, page)

        return data_out


@namespace.route("/get_result_attendance", methods=["GET"])
class ResultAttendance(Resource):
    def get(self):
        """
        Sẽ trả về kết quả dựa vào kết quả điểm danh của giáo viên lấy giáo viên làm chuẩn, chỉ có thiếu hoặc sai, không có dư.
        Nếu api nhận kết quả diểm danh rỗng thì trả về thông báo chưa có kết quả điểm danh từ giáo viên
        B1: Gọi api từ PHP lấy danh sách học sinh từ giáo viên theo thời gian, mặc định ngày hiện tại
        B2: Load data điểm danh từ db AI, lọc theo ngày trùng vs ngày hiện tại
        B3: Số hàng bảng so sánh mảng của giáo viên điểm danh,
            + Nếu user_id không có trên AI => thiếu.
            +
        :return:
        """

        limit = request.args.get('limit', default=None, type=int)
        page = request.args.get('page', default=None, type=int)
        branch_id = request.args.get('branch_id', default=None, type=str)
        class_id = request.args.get('class_id', default=None, type=str)
        from_date = request.args.get('fromDate', default=None, type=str)
        to_date = request.args.get('toDate', default=None, type=str)
        status_result_ai = request.args.get('status_result_ai', default=None, type=int)
        print("status_result_ai: ", status_result_ai)

        # Lấy dữ liệu giáo viên điểm danh từ giáo viên (PHP Đáng)
        payload = {}
        headers = {}
        response = requests.request("GET", url_report_attendance_teacher, headers=headers, data=payload)
        data_attendance_teacher = json.loads(response.text)['data']
        # Chỗ này Đáng cần gửi thêm class_id vs brand_id thì mới lọc được mới gửi tên.
        if len(data_attendance_teacher) == 0:
            options = {"status": True, "status_code": 200, "message": "Chưa có kết quả điểm danh từ giáo viên!",
                       "data": []}
            return options

        # Lấy kết quả điểm danh từ AI theo ngày.
        object_attendance_ai = object_dal.find_all_item()

        # Lọc lớp vs cơ sở
        if class_id is not None:
            # find id camera by branch_id
            id_cam = camera_dal.find_id_by_class_id(class_id=class_id)
            if len(id_cam) == 0:
                options = {"message": "class_id found any camera"}
                return options

            id_cam = str(id_cam[0]["_id"])
            process_name = id_cam + "_roll_call"
            new_item = []
            for i in range(len(object_attendance_ai)):
                if process_name in object_attendance_ai[i]["process_name"]:
                    new_item.append(object_attendance_ai[i])
            object_attendance_ai = new_item

        if branch_id is not None:
            # find id camera by branch_id
            new_item = []
            id_cam = camera_dal.find_id_by_branch_id(branch_id=branch_id)
            if len(id_cam) == 0:
                options = {"message": "branch_id found any camera"}
                return options

            id_cam = str(id_cam[0]["_id"])

            process_name = id_cam + "_roll_call"
            for i in range(len(object_attendance_ai)):
                if process_name in object_attendance_ai[i]["process_name"]:
                    new_item.append(object_attendance_ai[i])
            object_attendance_ai = new_item

        if from_date is not None and to_date is not None:
            new_item = []
            for i in range(len(object_attendance_ai)):
                hs = object_attendance_ai[i]
                date_time = hs["created_at"]
                seconds = date_time.timestamp()
                from_date_second = datetime.strptime(from_date, "%Y-%m-%d").timestamp()
                to_date_second = datetime.strptime(to_date, "%Y-%m-%d").timestamp()
                if seconds < to_date_second + 86400 and (seconds > from_date_second):
                    new_item.append(hs)
            object_attendance_ai = new_item

        list_user_id_attendance_ai = []
        for item in object_attendance_ai:
            hs_data = identity_dal.find_by_id(item["identity"])
            list_user_id_attendance_ai.append(hs_data["user_id"])
        assert len(list_user_id_attendance_ai) == len(object_attendance_ai)

        data_out = []
        for student in data_attendance_teacher:
            if student['user_id'] in list_user_id_attendance_ai:
                idx = list_user_id_attendance_ai.index(student['user_id'])
                data_out.append({
                    'id_object_attendance': str(object_attendance_ai[idx]["_id"]),
                    'name': student['name'],
                    'class_name': student['class_name'],
                    'branch_name': student['branch_name'],
                    'url_face': [object_attendance_ai[idx]['avatars'], object_attendance_ai[idx]['avatars_ori']],
                    'avatars_match': object_attendance_ai[idx]['avatars_match'],
                    'similarity_distance': object_attendance_ai[idx]['similarity_distance'],
                    'time_go_in_class': get_utc_time_from_datetime(object_attendance_ai[idx]["created_at"]),
                    "status_result_ai": True,
                    "result_ai": object_attendance_ai[idx]['result_ai'] if "result_ai" in object_attendance_ai[
                        idx] else "Unknown",
                })
            else:
                data_out.append({
                    # 'id_object_attendance': str(object_attendance_ai[idx]["_id"]),
                    'name': student['name'],
                    'class_name': student['class_name'],
                    'branch_name': student['branch_name'],
                    'avatars': None,
                    'avatars_ori': None,
                    'avatars_match': None,
                    'similarity_distance': None,
                    'time_go_in_class': None,
                    "status_result_ai": False,
                })

        '''
        {status_result_ai: 1, name: 'Tất cả kết quả'},
        {status_result_ai: 2, name: 'Camera có điểm danh'},
        {status_result_ai: 3, name: 'Camera không điểm danh được'}
        '''
        if status_result_ai == 2:
            new_item = []
            for i in range(len(data_out)):
                if data_out[i]["status_result_ai"]:
                    new_item.append(data_out[i])
            data_out = new_item

        if status_result_ai == 3:
            new_item = []
            for i in range(len(data_out)):
                if not data_out[i]["status_result_ai"]:
                    new_item.append(data_out[i])
            data_out = new_item

        data_out = pagination(limit, data_out, page)
        #
        return data_out


@namespace.route("/update_result_ai/<_id_object_attendance>", methods=["PUT"])
class FindById(Resource):
    def put(self, _id_object_attendance):
        request_data = request.json
        result_ai = request_data.get("result_ai")
        data_update = []
        if result_ai == 1:
            data_update.append({
                "result_ai": "Đúng"

            })
        if result_ai == 2:
            data_update.append({
                "result_ai": "Sai"
            })

        object_dal.update_document([_id_object_attendance], data_update)


@namespace.route("/report_date", methods=["GET"])
class FindById(Resource):
    def get(self):
        """
        :param limit, page, branch_cam, class_cam
        :return: get all data roll call from process _id + "_roll_call"
        Mongo Compass {process_name: "61d56d210d7c41e2668ec409_roll_call"}
        {process_name: "61d56d210d7c41e2668ec409_roll_call", have_new_face: true}
        Data format:
        """

        limit = request.args.get('limit', default=None, type=int)
        page = request.args.get('page', default=None, type=int)
        branch_id = request.args.get('branch_id', default=None, type=str)
        class_id = request.args.get('class_id', default=None, type=str)
        date = request.args.get('date', default=None, type=str)
        user_id = request.args.get('user_id', default=None, type=str)

        if user_id is not None and len(user_id) > 0:
            list_user_id_search = user_id.split(",")
        else:
            list_user_id_search = None

        item = object_dal.find_all_item()

        # Filter item item["have_new_face"] is True and sort time.
        new_item = []
        list_time = []
        for i in range(len(item)):
            hs = item[i]
            date_time = hs["created_at"]
            seconds = date_time.timestamp()
            if hs.get("identity_name") is not None:
                new_item.append(item[i])
                list_time.append(seconds)
        list_index_sort = np.argsort(np.array(list_time))[::-1]
        item = np.array(new_item)[list_index_sort]

        if date is not None:
            new_item = []
            for i in range(len(item)):
                hs = item[i]
                date_time = hs["created_at"]
                seconds = date_time.timestamp()
                from_date_second = datetime.strptime(date, "%Y-%m-%d").timestamp()
                if seconds <= from_date_second + 86400 and (seconds >= from_date_second):
                    new_item.append(hs)
            item = new_item

        if branch_id is not None:
            new_item = []
            for hs in item:
                if hs.get("identity") is not None:
                    hs_data = identity_dal.find_by_id(hs["identity"])
                    if hs_data is not None and hs_data["branch_id"] == branch_id:
                        new_item.append(hs)
            item = new_item

        if class_id is not None:
            new_item = []
            for hs in item:
                if hs.get("identity") is not None:
                    hs_data = identity_dal.find_by_id(hs["identity"])
                    # print("class_id in identity: ", hs_data["class_id"])
                    # print("class_id in filter: ", class_id)
                    if hs_data["class_id"] == class_id:
                        new_item.append(hs)
            item = new_item

        new_item = []
        for hs in item:
            object_info = get_object_roll_call_date(hs)
            if object_info is not None:
                new_item.append(object_info)
        item = new_item

        # Filter name in list_user_id_search
        if list_user_id_search is not None:
            new_item = []
            for hs in item:
                if hs["user_id"] in list_user_id_search:
                    new_item.append(hs)

        data_out = pagination(limit, new_item, page)

        return data_out


@namespace.route("/report_name", methods=["GET"])
class FindById(Resource):
    def get(self):
        """
        :param limit, page, branch_cam, class_cam, fromDate, toDate, user_id
        :return: get all data roll call from process _id + "_roll_call"
        Mongo Compass {process_name: "61d56d210d7c41e2668ec409_roll_call"}
        {process_name: "61d56d210d7c41e2668ec409_roll_call", have_new_face: true}
        Data format:
        """

        limit = request.args.get('limit', default=None, type=int)
        page = request.args.get('page', default=None, type=int)
        branch_id = request.args.get('branch_id', default=None, type=str)
        class_id = request.args.get('class_id', default=None, type=str)
        from_date = request.args.get('fromDate', default=None, type=str)
        to_date = request.args.get('toDate', default=None, type=str)
        user_id = request.args.get('user_id', default=None, type=str)

        if user_id is not None and len(user_id) > 0:
            list_user_id_search = user_id.split(",")
        else:
            list_user_id_search = None

        item = object_dal.find_all_item()

        # Filter item item["have_new_face"] is True and sort time.
        new_item = []
        list_time = []
        for i in range(len(item)):
            hs = item[i]
            date_time = hs["created_at"]
            seconds = date_time.timestamp()
            if hs.get("identity_name") is not None:
                # only filter hs was had recognition
                new_item.append(item[i])
                list_time.append(seconds)
        list_index_sort = np.argsort(np.array(list_time))[::-1]
        item = np.array(new_item)[list_index_sort]

        if from_date is not None and to_date is not None:
            new_item = []
            for i in range(len(item)):
                hs = item[i]
                date_time = hs["created_at"]
                seconds = date_time.timestamp()
                from_date_second = datetime.strptime(from_date, "%Y-%m-%d").timestamp()
                to_date_second = datetime.strptime(to_date, "%Y-%m-%d").timestamp()
                if seconds < to_date_second + 86400 and (seconds > from_date_second):
                    new_item.append(hs)
            item = new_item

        if branch_id is not None:
            new_item = []
            for hs in item:
                if hs.get("identity") is not None:
                    hs_data = identity_dal.find_by_id(hs["identity"])
                    if hs_data is not None and hs_data["branch_id"] == branch_id:
                        new_item.append(hs)
            item = new_item

        if class_id is not None:
            new_item = []
            for hs in item:
                if hs.get("identity") is not None:
                    hs_data = identity_dal.find_by_id(hs["identity"])
                    if hs_data is not None and hs_data["class_id"] == class_id:
                        new_item.append(hs)
            item = new_item

        # Get data out and filter name remain(trung ten)
        new_item = []
        list_name_remain = []
        for hs in item:
            remain, object_info = get_object_roll_call_name(hs, list_name_remain)
            if object_info is not None:
                if remain:
                    user_id_remain = object_info["user_id"]
                    for idx in range(len(new_item)):
                        if new_item[idx]["user_id"] == user_id_remain:
                            new_item[idx]["count_roll_call"] += 1
                            new_item[idx]["url_face"] += object_info["url_face"]
                            new_item[idx]["url_face_match"] += object_info["url_face_match"]
                            new_item[idx]["time_go_in_class"] += object_info["time_go_in_class"]
                            break
                else:
                    new_item.append(object_info)
        item = new_item

        # Filter name in list_user_id_search
        if list_user_id_search is not None:
            new_item = []
            for hs in item:
                if hs["user_id"] in list_user_id_search:
                    new_item.append(hs)

        data_out = pagination(limit, new_item, page)

        return data_out
