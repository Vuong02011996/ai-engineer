import multiprocessing as mp
import os
import re
import socket
import signal
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from bson import ObjectId
from flask import Blueprint, request
from flask_restx import Api, Resource
from sentry_sdk import capture_message

from app.mongo_dal.camera_dal import CameraDAL
from app.mongo_dal.identity_dal import IdentityDAL
from app.mongo_dal.object_dal.object_attendance_dal import ObjectAttendanceDAL
from app.mongo_dal.process_dal.process_attendance_dal import ProcessAttendanceDAL
from app.rabbit_mq_dal.publish_dal import PikaPublisher
from app.services.services_helper import update_status_job, get_frame_url_from_cam
from app.services.vms_face_detection.face_detection_model_with_oryza_AI import run_roll_call

blueprint = Blueprint("Face_Service", __name__)
# Using register_blueprint
api = Api(blueprint, title="Face_Service", version="1.0.0", description="Swagger API Homepage")

# Using namespace
# ns = Api(blueprint)
# namespace = ns.namespace("Face_Service")

# Sử dụng để viết api bất đồng bộ
executor_start_process = ThreadPoolExecutor(5)
executor_run_loop = ThreadPoolExecutor(5)

camera_dal = CameraDAL()
object_dal = ObjectAttendanceDAL()
process_dal = ProcessAttendanceDAL()
identity_dal = IdentityDAL()
start_server = True
start_server_for_run_loop = True

port_model_head = int(os.getenv("port_model_head"))
port_model_insight = int(os.getenv("port_model_insight"))
ip_run_service_insight = os.getenv("ip_run_service_insight")
ip_run_service_head = os.getenv("ip_run_service_head")
ip_run_service_ai = os.getenv("ip_run_service_ai")

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

# @namespace.route("/enable", methods=["POST"])
@api.route("/enable", methods=["POST"])
class StartById(Resource):
    def post(self):
        """
        Post json data:
        {
            "process_id": "9a5dcef8-8028-5c36-56b9-ee51381f454d",
            "rtsp": "rtsp://192.168.111.59:7001/9a5dcef8-8028-5c36-56b9-ee51381f454d",
        }
        Returns:

        """
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options

        id_camera = request_data.get("process_id")
        rtsp = request_data.get("rtsp")
        ip_camera = request_data.get("ip_camera")
        print("rtsp: ", rtsp)
        print("id_camera: ", id_camera)
        print("ip_camera: ", ip_camera)

        # save info camera if id camera not in table cameras in database
        id_cam_mg = camera_dal.find_id_by_id_camera(id_camera=id_camera)
        if len(id_cam_mg) == 0:
            camera_dal.create_one(
                {
                    "id_camera": id_camera,
                    "url_cam": rtsp,
                    "created_at": datetime.now(),
                }
            )
            print("Camera not in table cameras , created it")
            # TypeError: id must be an instance of (bytes, str, ObjectId), not <class 'list'> => much add
            id_cam_mg = camera_dal.find_id_by_id_camera(id_camera=id_camera)
            id_cam_mg = str(id_cam_mg[0]["_id"])
            camera_id = ObjectId(id_cam_mg)
            item_cam = camera_dal.find_by_id(camera_id)
        else:
            id_cam_mg = str(id_cam_mg[0]["_id"])
            camera_id = ObjectId(id_cam_mg)

            data_update = {
                "id_camera": id_camera,
                "url_cam": rtsp,
                "created_at": datetime.now(),
            }
            camera_dal.update({"_id": camera_id}, data_update)
            item_cam = camera_dal.find_by_id(camera_id)
            print("Camera existed in table cameras")
            print("Update all info cam")

        # check if start server all process of camera is running must stop, if stop incorrect
        # Trường hợp mới start server thì tất cả process phải stop(sửa lỗi trường hợp process không được stop đúng cách)

        global start_server
        if start_server:
            # list_all_item_process = process_dal.find_all_item()
            # for process in list_all_item_process:
            #     if process["status_process"] != "Stop":
            #         data_update = {
            #             "status_process": "Stop",
            #         }
            #         process_dal.update({"_id": process["_id"]}, data_update)
            print("all process is delete when start server: ")
            # process_dal.drop_collection()
            start_server = False

        #  Kiểm tra nếu cam id đang chạy điểm danh thì return
        # ở đây có thể check bằng process_id hoặc bằng process_name

        list_all_item_process = process_dal.find_all_item()
        for p in list_all_item_process:
            if p["process_name"].split("_")[0] == id_cam_mg and p["status_process"] == "running" and (
                    "roll_call" in p["process_name"]):
                print("Camera is running attendance, process_name is {}".format(p["process_name"]))
                # options = {"status": False, "status_code": 200, "message": "Camera is running attendance! You can kill and enable again"}
                options = {"process_id": id_camera, "status": "already", "pid": p["multiprocessing_pid"]}
                return options

        # Check camera đã lưu cấu hình nhiệm vụ hay chưa.
        # if item_cam.get("jobs_cam") is None or item_cam["jobs_cam"].get("roll_call") is None:
        #     print("Cam cannot start, Camera chưa cấu hình vùng điểm danh")
        #     options = {"status": False, "status_code": 500, "message": "Camera chưa cấu hình vùng điểm danh"}
        #     return options

        # Get from time and end time to start and kill process
        time_utc_now = datetime.utcnow()
        time_now = datetime.now()
        time_now_seconds = time_utc_now.timestamp()
        end_time_s = time_now_seconds

        # if time_now_seconds > end_time_s or time_now_seconds < from_time_s:
        #     print("Cam cannot start, Thời gian hiện tại nằm ngoài thời điểm để điểm danh!")
        #     options = {"status": False, "status_code": 500,
        #                "message": "Thời gian hiện tại nằm ngoài thời điểm để điểm danh"}
        #     return options

        # Create new process
        process_name = id_camera + "_" + id_cam_mg + "_roll_call_" + str(len(process_dal.find_all_item())) + "_" + \
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

                address = ""
                info_cam_running = {
                    "port_model_head": port_model_head,
                    "port_model_insight": port_model_insight,
                    "ip_camera": ip_camera,
                    "ip_run_service_head": ip_run_service_head,
                    "ip_run_service_insight": ip_run_service_insight,
                    "ip_run_service_ai": ip_run_service_ai,
                    "address": address,
                    "process_name": process_name,

                }
                process = mp.Process(target=run_roll_call,
                                     args=(item_cam, end_time_s, info_cam_running, False))
                multiprocessing_pid = process.pid
                print("Before start multiprocessing_pid: ", multiprocessing_pid)
                process.start()
                multiprocessing_pid = process.pid
                print("After start multiprocessing_pid: ", multiprocessing_pid)
                #  Create process data in mongoDB

                data_process = {
                    "process_name": process_name,
                    "process_id": id_camera,
                    "multiprocessing_pid": multiprocessing_pid,
                    "status_process": "running",
                    # "camera": item_cam["_id"],
                    "camera": id_cam_mg,
                    "created_at": datetime.now(),
                }
                process_dal.create_one(data_process)
                # Update status in jobcam roll call is RUNNING in table cameras, but current not work

                # update_status_job(item_cam["_id"], item_cam, process_name, status_process="running",
                #                   job="roll_call")
                print("Create process on DB success...process is running")

                process.join()
                process.terminate()
                # If process finished find process_id and change status to stop
                process_id = process_dal.find_object_id_by_process_name(process_name)
                print("Process finished , change status process to not_run")
                data_update = {
                    "status_process": "not_run",
                    "created_at": datetime.now(),
                }
                if len(process_id) > 0:
                    process_dal.update({"_id": process_id[0]["_id"]}, data_update)
                    print("process_name {} Stop".format(process_name))

                # Update status in jobcam roll call is NOT_RUN
                # update_status_job(item_cam["_id"], item_cam, process_name, status_process="not_run",
                #                   job="roll_call")
                options = {"status": True, "status_code": 200, "process_name": process_name,
                           "status_process": "not_run",
                           "message": "process_name is stop "}
                return options

            #  xử lí api bất đồng bộ
            executor_start_process.submit(process_data)
            # options = {"status": True, "status_code": 200, "process_name": process_name,
            #            "status_process": "running",
            #            "message": "Setup camera to success! Attendance is running on camera"}
            # return options

            options = {"process_id": id_camera, "status": "started", "pid": None}
            return options

        except RuntimeError:
            # options = {"status": False, "status_code": 500, "process_name": process_name,
            #            "status_process": "not_run",
            #            "message": "Setup camera error , can't run attendance on camera"}
            options = {"process_id": id_camera, "status": "error", "pid": None, "message": "Setup camera error , can't run attendance on camera"}
            capture_message("Setup camera error , can't start attendance on camera")
            return options


# @namespace.route("/kill", methods=["POST"])
@api.route("/kill", methods=["POST"])
class StartById(Resource):
    def post(self):
        """
        Post json data:
        {
            "process_id": "9a5dcef8-8028-5c36-56b9-ee51381f454d",
        }
        Returns:

        """

        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options

        id_camera = request_data.get("process_id")
        print("Kill process_id/id_camera: ", id_camera)
        # Stop camera
        id_cam_mg = camera_dal.find_id_by_id_camera(id_camera=id_camera)
        if len(id_cam_mg) == 0:
            options = {"status": True, "status_code": 200,
                       "id_camera": id_camera,
                       "status_process": "not_run",
                       "message": "id_camera not running attendance!"}
            return options

        #  Kiểm tra nếu cam id đang chạy điểm danh thì stop
        id_cam_mg = str(id_cam_mg[0]["_id"])
        list_all_item_process = process_dal.find_all_item()
        for p in list_all_item_process:
            if p["process_name"].split("_")[0] == id_cam_mg and p["status_process"] == "running" and (
                    "roll_call" in p["process_name"]):
                print("Have process is running attendance, process_name is {}".format(p["process_name"]))
                process_name = p["process_name"]
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
                    # options = {"status": True, "status_code": 200,
                    #            "process_name": process_name,
                    #            "status_process": "not_run",
                    #            "message": "Process name no exist in database!"}
                    options = {"process_id": id_camera, "status": "not found"}

                    return options

                # options = {"status": True, "status_code": 200,
                #            "process_name": process_name,
                #            "status_process": "not_run",
                #            "message": "Stop attendance on camera success!"}
                options = {"process_id": id_camera, "status": "stopped"}

                return options

        # options = {"status": True, "status_code": 200,
        #            "status_process": "not_run",
        #            "message": "Camera not run attendance! Can't kill process!"}
        options = {"process_id": id_camera, "status": "not found"}
        return options


# @namespace.route("/get_status_process", methods=["POST"])
@api.route("/get_status_process_id", methods=["POST"])
class StartById(Resource):
    def post(self):
        """
        Post json data:
        {
            "process_id": "9a5dcef8-8028-5c36-56b9-ee51381f454d",
        }
        Returns:
        """
        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options

        id_camera = request_data.get("process_id")
        print("Get status process_id/id_camera: ", id_camera)
        # Stop camera
        id_cam_mg = camera_dal.find_id_by_id_camera(id_camera=id_camera)
        if len(id_cam_mg) == 0:
            options = {"status": True, "status_code": 200,
                       "id_camera": id_camera,
                       "status_process": "not_run",
                       "message": "id_camera not running detect face!"}
            return options

        #  Kiểm tra nếu cam id đang chạy điểm danh thì stop
        id_cam_mg = str(id_cam_mg[0]["_id"])
        # List all process of camera
        list_all_item_process = process_dal.find_all_item()
        for p in list_all_item_process:
            process_name = p["process_name"]
            status_process = p["status_process"]
            if process_name.split("_")[0] == id_cam_mg and status_process == "running" and (
                    "roll_call" in process_name):
                print("Camera is running roll call, process_name is {}".format(process_name))
                print("process_name: ", process_name)
                info_cam = process_dal.find_camera_by_process_name(process_name)
                if len(info_cam) == 0:
                    options = {"status": True, "status_code": 200,
                               "process_id": id_camera,
                               "process_name": process_name,
                               "status_process": "not_run",
                               "message": "Process name no exist in database!"}

                    return options

                options = {"status": True, "status_code": 200,
                           "process_id": id_camera,
                           "process_name": process_name,
                           "status_process": status_process,
                           "message": "Get status process success"}

                return options
        options = {"status": True, "status_code": 200,
                   "process_id": id_camera,
                   "status_process": "not_run",
                   "message": "Camera not run attendance!"}
        return options


def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipV4 = s.getsockname()[0]
    s.close()
    return ipV4


# @namespace.route("/get_status_process", methods=["POST"])
@api.route("/get_status_all_process", methods=["GET"])
class StartById(Resource):
    def get(self):
        """
        Returns:
            return status all process of camera
            and run one loop 5s will send status all process.
        """
        global start_server_for_run_loop
        if start_server_for_run_loop:

            # If start service all process is delete
            print("all process is delete when start server: ")
            """Có thể xóa chỗ này vì vẫn chưa gọi api enable khi mới start server nên vẫn chưa tạo process 
            Bên BE chỉ tạo gọi enable và tạo process khi có tín hiệu quả tới rabbitMQ check server đang hoạt động 
            Tức là sau khi chạy qua dòng này mới tạo process """
            process_dal.drop_collection()
            start_server_for_run_loop = False

            def process_loop_send_status():
                # processCustom = ProcessCustom()
                pikaPublisher = PikaPublisher()
                ip = get_ipv4_address()
                print("ip v4: ", ip)

                while True:
                    # list_check = {}
                    # for id in processCustom.obj_process:
                    #     list_check[id] = processCustom.obj_process[id].is_alive()
                    # data_send['data'] = list_check
                    list_all_item_process = process_dal.find_all_item()
                    info_data = {}

                    for p in list_all_item_process:
                        status_process = p["status_process"]
                        # Process khi tạo bên VMS sẽ không có process_id như tạo bên oryza AI
                        if p.get("process_id") is not None:
                            process_id = p["process_id"]
                            # if status_process == "running":
                                # print("process_id: ", process_id)
                                # print("status_process: ", status_process)
                            info_data[process_id] = True if status_process == "running" else False

                    data_send = {'ip': ip, 'port': 30000,
                                 'data': info_data}
                    pikaPublisher = PikaPublisher()
                    pikaPublisher.send_message(data=data_send, exchange_name='CHECK_STATUS_SERVER_EXCHANGES')
                    time.sleep(5)
                    print("Send data to rabbitMQ every 5s data_send: ", data_send)

            executor_run_loop.submit(process_loop_send_status)
            options = {"status": True, "status_code": 200,
                       "message": "Run loop get status process!"}

            return options
        else:
            print("Run loop get status all process is running on service!")
            options = {"status": True, "status_code": 200,
                       "message": "Run loop get status all process is running on service! ",
                       "start_server_for_run_loop": start_server_for_run_loop}

            return options


"""
Sau khi pm2 stop service , process is running not change status in DB
After start again after call api enable , moi stop all process 
Khong the stop all process ben ngoai api, vi khi mot camera moi chayj se chay lai file service 
Hien tai:
After start server, go into DB change status process to Stop.
"""


