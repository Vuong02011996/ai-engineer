import signal
import os
import cv2
from datetime import datetime
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from bson import ObjectId

from app.app_utils.file_io_untils import upload_img_from_disk

from app.services.services_helper import pagination
from app.mongo_dal.camera_dal import CameraDAL
from app.mongo_dal.object_dal.object_attendance_dal import ObjectAttendanceDAL
from app.mongo_dal.process_dal.process_attendance_dal import ProcessAttendanceDAL
from app.mongo_models.camera import StatusCam

blueprint = Blueprint("Cameras", __name__)
ns = Api(blueprint)
namespace = ns.namespace("Cameras")

camera_dal = CameraDAL()
object_dal = ObjectAttendanceDAL()
process_dal = ProcessAttendanceDAL()

thread_manager = []
list_process_stream = []
list_url_stream = []


@namespace.route("/register", methods=["POST"])
class FindAll(Resource):
    def post(self):
        """
        Create a new camera with general information
        :param json file
        Example
       {
            "name_cam" : "Camera1",
            "branch_cam" : "Lake View",
            "branch_id" : "1111-1111-1111-555",
            "class_cam" : "Preschool1",
            "class_id" : "1111-1111-1111-556",
            "position_cam" : "Góc trên bên trái phòng",
            "position_id" : "1111-1111-1111-557",
            "ip_cam" : "14.241.120.239",
            "port_cam" : "554",
            "username_cam" : "admin",
            "password_cam" : "Admin123",
            "status_cam" : "DISCONNECT"
        }
        :return:
        {
            "status": true,
            "status_code": 200,
            "message": "Register a camera successfully!"
        }
        """
        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options

        name_cam = request_data.get("name_cam")
        # print("username register", username)
        branch_cam = request_data.get("branch_cam")
        branch_id = request_data.get("branch_id")
        class_cam = request_data.get("class_cam")
        class_id = request_data.get("class_id")
        position_cam = request_data.get("position_cam")
        position_id = request_data.get("position_id")
        ip_cam = request_data.get("ip_cam")
        port_cam = request_data.get("port_cam")
        username_cam = request_data.get("username_cam")
        password_cam = request_data.get("password_cam")

        if request_data.get("url_cam") is not None:
            url_cam = request_data.get("url_cam")
        else:
            url_cam = "rtsp://" + username_cam + ":" + password_cam + "@" + ip_cam + ":" + port_cam

        camera_dal.create_one(
            {
                "name_cam": name_cam,
                "branch_cam": branch_cam,
                "branch_id": branch_id,
                "class_cam": class_cam,
                "class_id": class_id,
                "position_cam": position_cam,
                "position_id": position_id,
                "ip_cam": ip_cam,
                "port_cam": port_cam,
                "username_cam": username_cam,
                "password_cam": password_cam,
                "url_cam": url_cam,
                "status_cam": StatusCam.DISCONNECT.value,
                "created_at": datetime.now(),
            }
        )

        options = {"status": True, "status_code": 200, "message": "Register a camera successfully!"}
        return options


@namespace.route("/update/<_id>", methods=["GET", "PUT", "DELETE"])
class FindById(Resource):
    def put(self, _id):
        """
        Update info a new camera
        Example: Put json
        {
            "name_cam" : "Camera1",
            "branch_cam" : "Lake View2",
            "branch_id" : "1111-1111-1111-555",
            "class_cam" : "Preschool1",
            "class_id" : "1111-1111-1111-556",
            "position_cam" : "Góc trên bên trái phòng",
            "position_id" : "1111-1111-1111-557",
            "ip_cam" : "14.241.120.239",
            "port_cam" : "554",
            "username_cam" : "admin",
            "password_cam" : "Admin123",
            "status_cam" : "DISCONNECT"
        }
        :param _id:  mongo id camera Ex http://14.241.120.239:8001/clover/test/v2.0/api/cameras/update/618a4408a71ca0ac64b1df02
        :return:
        {
            "status": true,
            "status_code": 200,
            "message": "Update a camera successfully!"
        }
        """
        # check _id have in mongo
        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options
        name_cam = request_data.get("name_cam")
        branch_cam = request_data.get("branch_cam")
        branch_id = request_data.get("branch_id")
        class_cam = request_data.get("class_cam")
        class_id = request_data.get("class_id")
        position_cam = request_data.get("position_cam")
        position_id = request_data.get("position_id")
        ip_cam = request_data.get("ip_cam")
        port_cam = request_data.get("port_cam")
        username_cam = request_data.get("username_cam")
        password_cam = request_data.get("password_cam")
        status_cam = request_data.get("status_cam")

        mongo_id = ObjectId(_id)
        if mongo_id is not None:  # UPDATE
            # mongo_id = mongo_id["_id"]
            item = camera_dal.find_by_id(mongo_id)
            if item is None:
                options = {"status": False, "status_code": 404, "message": "Cam id not found in database"}
                return options
            name_cam = name_cam if name_cam is not None else item["name_cam"]
            branch_cam = branch_cam if branch_cam is not None else item["branch_cam"]
            branch_id = branch_id if branch_id is not None else item["branch_id"]
            class_cam = class_cam if class_cam is not None else item["class_cam"]
            class_id = class_id if class_id is not None else item["class_id"]
            position_cam = position_cam if position_cam is not None else item["position_cam"]
            position_id = position_id if position_id is not None else item["position_id"]
            ip_cam = ip_cam if ip_cam is not None else item["ip_cam"]
            port_cam = port_cam if port_cam is not None else item["port_cam"]
            username_cam = username_cam if username_cam is not None else item["username_cam"]
            password_cam = password_cam if password_cam is not None else item["password_cam"]


            # open the feed
            url_cam = "rtsp://" + username_cam + ":" + password_cam + "@" + ip_cam + ":" + port_cam
            cap = cv2.VideoCapture(url_cam)
            ret, frame = cap.read()
            if ret:
                frame_url = upload_img_from_disk(
                    image_name=username_cam + "_" + password_cam + "_" + ip_cam + "_" + port_cam,
                    img_arr=frame)
                status_cam = StatusCam.CONNECT.value
            else:
                frame_url = None
                status_cam = StatusCam.DISCONNECT.value

            data_update = {
                "name_cam": name_cam,
                "branch_cam": branch_cam,
                "branch_id": branch_id,
                "class_cam": class_cam,
                "class_id": class_id,
                "position_cam": position_cam,
                "position_id": position_id,
                "ip_cam": ip_cam,
                "port_cam": port_cam,
                "username_cam": username_cam,
                "password_cam": password_cam,
                "status_cam": status_cam,
                "frame_url": frame_url,
                "url_cam": url_cam,
                "created_at": datetime.now(),
            }

            camera_dal.update({"_id": mongo_id}, data_update)
        options = {"status": True, "status_code": 200, "message": "Update a camera successfully!"}

        return options


# @namespace.route("/status_jobs/<_id>", methods=["GET"])
# class FindById(Resource):
#     def get(self, _id):
#         """
#         Get status about job of each camera
#         :param _id:
#         :return:
#         {
#             "cam_id": "61dbe1b3889b4d0b52ca64f0",
#             "jobs_status": [
#                 {
#                     "name_job": "roll_call",
#                     "status_job": "running"
#                 },
#                 {
#                     "name_job": "safe_region",
#                     "status_job": "running"
#                 }
#             ]
#         }
#         """
#         mongo_id = ObjectId(_id)
#         data_jobs = []
#
#         item = camera_dal.find_by_id(mongo_id)
#         if item is None:
#             data_out = {
#                 "cam_id": None,
#                 "jobs_status": data_jobs,
#                 "message": "cam_id not found in database"
#             }
#             return data_out
#
#         # # check stream_status if stop or None , stream again
#         # url_cam = item["url_cam"]
#         # stream_url = item["stream_url"]
#         # url_stream_server = item["url_stream_server"]
#         # print('list_url_stream', list_url_stream)
#         # print('url_stream', stream_url)
#         #
#         # if stream_url not in list_url_stream and len(list_url_stream) == 0:
#         #     process_stream, fps, width, height = create_process_stream(url_cam, url_stream_server)
#         #     t = KThread(target=stream_url_cam, args=(url_cam, process_stream))
#         #     t.daemon = True
#         #     t.start()
#         #     thread_manager.append(t)
#         #     list_process_stream.append(process_stream)
#         #     list_url_stream.append(stream_url)
#
#         # find list process from camera id
#         list_process_id = process_dal.find_object_id_by_camera_id(mongo_id)
#
#         for process_id in list_process_id:
#             data_process = process_dal.find_by_id(process_id["_id"])
#             status_process = data_process["status_process"]
#             name_job = data_process["process_name"].split("_", 1)[1]
#             jobs = {
#                 "name_job": name_job,
#                 "status_job": status_process
#             }
#             data_jobs.append(jobs)
#
#         data_out = {
#             "cam_id": str(item["_id"]),
#             "jobs_status": data_jobs,
#             "message": "Get status jobs successfully"
#         }
#         return data_out
#
#
# @namespace.route("/check_connect_camera/<_id>", methods=["POST"])
# class FindAll(Resource):
#     def post(self, _id):
#         """
#         Check camera active.
#         :param _id: id camera , post json file
#         Example
#        {            "ip_cam" : "14.241.120.239",            "port_cam" : "554",            "username_cam" : "admin",
#             "password_cam" : "Admin123"
#         }
#         :return:
#         {
#             "status": true,
#             "status_code": 200,
#             "message": "Connect camera successfully!"
#         }
#         """
#         # get id cam, if connected don't stream and connect again.
#         request_data = request.json
#         if not request_data:
#             options = {"status": False, "status_code": 404, "message": "Resource not found"}
#             return options
#
#         ip_cam = request_data.get("ip_cam")
#         port_cam = request_data.get("port_cam")
#         username_cam = request_data.get("username_cam")
#         password_cam = request_data.get("password_cam")
#
#         # url_cam = "rtsp://admin:Admin123@14.241.120.239:554"
#         url_cam = "rtsp://" + username_cam + ":" + password_cam + "@" + ip_cam + ":" + port_cam
#         mongo_id = ObjectId(_id)
#
#         # open the feed
#         cap = cv2.VideoCapture(url_cam)
#         ret, frame = cap.read()
#         if ret:
#             frame_url = upload_img_from_disk(image_name=username_cam + "_" + password_cam + "_" + ip_cam + "_" + port_cam,
#                                              img_arr=frame)
#
#             # url_stream = "http://14.241.120.239:55557/stream/test.flv"
#             # How to auto add more local path to file nginx config and get domain stream for camera in here
#             stream_url = "https://stream.clover.greenlabs.ai/"
#             url_stream_server = "rtmp://0.0.0.0:55555/stream/test"
#
#             options = {"status": True, "status_code": 200, "message": "Connect camera successfully!", "url_cam": url_cam,
#                        "frame_url": frame_url, "stream_url": stream_url, "url_stream_server": url_stream_server}
#
#             data_update = {
#                 "ip_cam": ip_cam,
#                 "port_cam": port_cam,
#                 "username_cam": username_cam,
#                 "password_cam": password_cam,
#                 "url_cam": url_cam,
#                 "url_stream_server": url_stream_server,
#                 "frame_url": frame_url,
#                 "stream_url": stream_url,
#                 "status_cam": StatusCam.CONNECT.value,
#                 "created_at": datetime.now(),
#             }
#         else:  # camera disconnect
#             options = {"status": False, "status_code": 200, "message": "Connect camera fail!", "url_cam": url_cam,
#                        "frame_url": None, "stream_url": None, "url_stream_server": None}
#
#             data_update = {
#                 "ip_cam": ip_cam,
#                 "port_cam": port_cam,
#                 "username_cam": username_cam,
#                 "password_cam": password_cam,
#                 "url_cam": url_cam,
#                 "url_stream_server": None,
#                 "stream_url": None,
#                 "frame_url": None,
#                 "status_cam": StatusCam.DISCONNECT.value,
#                 "created_at": datetime.now(),
#             }
#         # close the connection
#         cap.release()
#
#         camera_dal.update({"_id": mongo_id}, data_update)
#
#         return options
#
#
# @namespace.route("/get_all_info_cam", methods=["GET"])
# class GetInfoCam(Resource):
#     def get(self):
#         """
#         Get info all camera in database
#         :return: info all camera
#         [
#             {
#                 "name_cam": "Camera1",
#                 "cam_id": "618cdc44a71ca0ac64b1df05",
#                 "branch_cam": "Lake View",
#                 "branch_id": "1111-1111-1111-555",
#                 "class_cam": "Preschool1",
#                 "class_id": "1111-1111-1111-556",
#                 "position_cam": "Góc trên bên trái phòng",
#                 "position_id": "1111-1111-1111-557",
#                 "ip_cam" : "14.241.120.239",
#                 "port_cam" : "554",
#                 "username_cam" : "admin",
#                 "password_cam" : "Admin123",
#                 "status_cam": "PENDING"
#             },
#             ...
#         ],
#          "meta": {
#                    "pagination": {
#                        "total": 26,
#                        "current_page": 1,
#                        "total_pages": 26
#                    }
#                },
#
#         """
#         limit = request.args.get('limit', default=None, type=int)
#         page = request.args.get('page', default=None, type=int)
#         status = request.args.get('status', default=None, type=str)
#         branch_id = request.args.get('branch_id', default=None, type=str)
#         class_id = request.args.get('class_id', default=None, type=str)
#         key_word = request.args.get('keyWord', default=None, type=str)
#
#         if status is not None:
#             item = camera_dal.find_all_by_condition_field("status_cam", status)
#         else:
#             item = camera_dal.find_all_item()
#
#         if branch_id is not None:
#             for i in range(len(item)):
#                 if item[i]["branch_id"] == branch_id:
#                     item = [item[i]]
#                     break
#             else:
#                 item = []
#
#         if class_id is not None:
#             for i in range(len(item)):
#                 if item[i]["class_id"] == class_id:
#                     item = [item[i]]
#                     break
#             else:
#                 item = []
#
#         if key_word is not None:
#             for i in range(len(item)):
#                 if item[i]["name_cam"] == key_word:
#                     item = [item[i]]
#                     break
#             else:
#                 item = []
#
#         new_item = []
#         for cam in item:
#             cam_info = {
#                 "name_cam": cam["name_cam"],
#                 "cam_id": str(cam["_id"]),
#                 "branch_cam": cam["branch_cam"],
#                 "branch_id": cam["branch_id"],
#                 "class_cam": cam["class_cam"],
#                 "class_id": cam["class_id"],
#                 "position_cam": cam["position_cam"],
#                 "position_id": cam["position_id"],
#                 "ip_cam": cam["ip_cam"],
#                 "port_cam": cam["port_cam"],
#                 "frame_url": None if cam.get("frame_url") is None else cam["frame_url"],
#                 "username_cam": cam["username_cam"],
#                 "password_cam": cam["password_cam"],
#                 "status_cam": cam["status_cam"],
#             }
#             new_item.append(cam_info)
#
#         data_out = pagination(limit, new_item, page)
#
#         return data_out
#
#
# @namespace.route("/cam_id/<_id>", methods=["GET", "DELETE"])
# class GetInfoCam(Resource):
#     def get(self, _id):
#         """
#         Get info one camera from id
#         :param _id: Ex http://14.241.120.239:8001/clover/test/v2.0/api/cameras/cam_id/618cdc44a71ca0ac64b1df05
#         :return:
#             {
#                 "name_cam": "Camera1",
#                 "cam_id": "618cdc44a71ca0ac64b1df05",
#                 "branch_cam": "Lake View",
#                 "branch_id": "1111-1111-1111-555",
#                 "class_cam": "Preschool1",
#                 "class_id": "1111-1111-1111-556",
#                 "position_cam": "Góc trên bên trái phòng",
#                 "position_id": "1111-1111-1111-557",
#                 "ip_cam" : "14.241.120.239",
#                 "port_cam" : "554",
#                 "username_cam" : "admin",
#                 "password_cam" : "Admin123",
#                 "stream_url": "https://stream.clover.greenlabs.ai/",
#                 "status_cam": "DISCONNECT"
#             }
#         """
#         mongo_id = ObjectId(_id)
#         item = camera_dal.find_by_id(mongo_id)
#
#         cam = item
#         cam_info = {
#             "name_cam": cam["name_cam"],
#             "cam_id": str(cam["_id"]),
#             "branch_cam": cam["branch_cam"],
#             "branch_id": cam["branch_id"],
#             "class_cam": cam["class_cam"],
#             "class_id": cam["class_id"],
#             "position_cam": cam["position_cam"],
#             "position_id": cam["position_id"],
#             "ip_cam": cam["ip_cam"],
#             "port_cam": cam["port_cam"],
#             "username_cam": cam["username_cam"],
#             "password_cam": cam["password_cam"],
#             "status_cam": cam["status_cam"],
#             "frame_url": None if cam.get("frame_url") is None else cam["frame_url"],
#             "stream_url": cam["stream_url"] if cam.get("stream_url") is not None else None,
#             "jobs_cam": cam["jobs_cam"] if cam.get("jobs_cam") is not None else {},
#         }
#         return cam_info
#
#     def delete(self, _id):
#         """
#         Delete a camera from id
#         :param _id: Ex http://14.241.120.239:8001/clover/test/v2.0/api/cameras/cam_id/618cdc44a71ca0ac64b1df05
#         :return:
#         {
#             "message": "Camera is deleted successfully"
#         }
#         """
#
#         id_cam = ObjectId(_id)
#         item = camera_dal.delete({"_id": id_cam})
#         options = {"message": "Camera is deleted successfully"}
#
#         # Get all process in database, find process using camera id was deleted.
#         process_item = process_dal.find_all_item()
#         for process in process_item:
#             process_name = process["process_name"]
#             if process_name.split("_")[0] == _id:
#                 # delete process and all object by process name
#                 process_dal.delete({"_id": process["_id"]})
#                 object_dal.delete_all_by_process_name(process_name)
#
#         # delete thread stream and process stream
#         for p in list_process_stream:
#             os.killpg(os.getpgid(p.pid), signal.SIGTERM)
#             print("Stop list_process_stream")
#         for t in thread_manager:
#             if t.is_alive():
#                 t.terminate()
#                 print("Stop thread_manager")
#         return options




