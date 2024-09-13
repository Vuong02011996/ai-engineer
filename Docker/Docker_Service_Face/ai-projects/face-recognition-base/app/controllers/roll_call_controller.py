import numpy as np
import multiprocessing
import signal
import os
import time
from datetime import datetime
from flask import Blueprint, request
from flask_restx import Api, Resource
from bson import ObjectId

# from app.app_utils.minio_utils import upload_image
from app.controllers.controller_helper import create_process_stream, get_object_info_roll_call, \
    get_object_roll_call_date, get_object_roll_call_name, pagination
from app.mongo_dal.camera_dal import CameraDAL
from app.mongo_dal.identity_dal import IdentityDAL
from app.mongo_dal.object_dal import ObjectDAL
from app.mongo_dal.process_dal import ProcessDAL
from app.services.attendance.attendance_model import run_roll_call

blueprint = Blueprint("Roll_Call", __name__)
ns = Api(blueprint)
namespace = ns.namespace("Roll_Call")

camera_dal = CameraDAL()
object_dal = ObjectDAL()
process_dal = ProcessDAL()
identity_dal = IdentityDAL()

process_manager = []
thread_roll_call_manager = []
list_process_stream = []

stop = False
start_server = True


@namespace.route("/update/<_id>", methods=["GET", "PUT", "DELETE"])
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
        # check _id have in mongo
        # get data
        request_data = request.json
        if not request_data:
            options = {"status": False, "status_code": 404, "message": "Resource not found"}
            return options
        jobs_cam = request_data.get("jobs_cam")

        # mongo_id = camera_dal.find_one_by_condition({"name_cam": name_cam}, columns={"_id": 1})
        mongo_id = ObjectId(_id)
        item_cam = camera_dal.find_by_id(_id)
        if item_cam.get("jobs_cam") is not None:
            jobs_cam_update = item_cam["jobs_cam"]
        else:
            jobs_cam_update = {}

        if jobs_cam is not None:
            if jobs_cam.get("roll_call") is not None:
                jobs_cam_update["roll_call"] = jobs_cam["roll_call"]

        data_update = {
            "jobs_cam": jobs_cam_update,
            "created_at": datetime.now(),
        }

        camera_dal.update({"_id": mongo_id}, data_update)
        options = {"status": True, "status_code": 200, "message": "Update a camera successfully!"}

        return options


@namespace.route("/start/<_id>", methods=["GET"])
class FindById(Resource):
    def get(self, _id):
        """
        :param _id:
        :return:
        """

        # check if start server all process is running must stop, if stop incorrect
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

        list_all_item_process = process_dal.find_all_item()
        for p in list_all_item_process:
            if p["process_name"].split("_")[0] == _id and p["status_process"] == "running" and ("roll_call" in p["process_name"]):
                print("Camera is running roll call, process_name is {}".format(p["process_name"]))
                options = {"status": True, "status_code": 200, "message": "Camera is running roll call!"}
                return options
                # time_start_p = p["process_name"].split("_")[-1]

        mongo_id = ObjectId(_id)
        item_cam = camera_dal.find_by_id(mongo_id)
        url_cam = item_cam["url_cam"]

        # Check camera đã lưu cấu hình nhiệm vụ hay chưa.
        if item_cam.get("jobs_cam") is None or item_cam["jobs_cam"].get("roll_call") is None:
            print("Cam cannot start, Camera haven't saved config region!")
            options = {"status": False, "status_code": 200, "message": "Camera haven't saved config region!"}
            return options

        # Get from time and end time to start and kill process
        time_now = datetime.utcnow()

        format_time = "%Y-%m-%dT%H:%M:%S.%fZ"
        from_time_roll_call = item_cam["jobs_cam"]["roll_call"]["from_time"]
        end_time_roll_call = item_cam["jobs_cam"]["roll_call"]["to_time"]
        from_time_roll_call_str = time_now.strftime("%Y-%m-%d") + "T" + from_time_roll_call.split("T")[-1]
        end_time_roll_call_str = time_now.strftime("%Y-%m-%d") + "T" + end_time_roll_call.split("T")[-1]
        # Convert string time to datetime
        from_time_roll_call_dt = datetime.strptime(from_time_roll_call_str, format_time)
        end_time_roll_call_dt = datetime.strptime(end_time_roll_call_str, format_time)
        from_time_roll_call_s = from_time_roll_call_dt.timestamp()
        end_time_roll_call_s = end_time_roll_call_dt.timestamp()

        # Create new process
        process_name = _id + "_roll_call_" + str(len(process_dal.find_all_item())) + "_" + \
                       datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        print(process_name)

        # For Streaming -----------------------------------------------------------
        url_stream_server = "rtmp://0.0.0.0:55555/stream/roll_call"
        process_stream, fps, width, height = create_process_stream(url_cam, url_stream_server, stream=False)
        if process_stream is not None:
            list_process_stream.append(process_stream)

        process_id = process_dal.find_object_id_by_process_name(process_name)
        if len(process_id) > 0:
            for i in range(len(process_id)):
                process_dal.delete({"_id": process_id[i]["_id"]})

        #  Create process data in mongoDB
        data_process = {
            "process_name": process_name,
            "url_cam": url_cam,
            "url_stream_server": url_stream_server,
            "fps_cam": fps,
            "width_cam": width,
            "height_cam": height,
            "status_process": "running",
            "job_process": "roll_call",
            "camera": mongo_id,
            "created_at": datetime.now(),
        }
        process_dal.create_one(data_process)

        global stop
        while True:
            # Get time current
            # Get from time and end time to start and kill process
            # Sleep less utc, roll_call now
            time_now = datetime.utcnow()
            time_now_seconds = time_now.timestamp()

            print("time_now_seconds: ", time_now_seconds)
            print("from_time_roll_call_s: ", from_time_roll_call_s)
            print("end_time_roll_call_s: ", end_time_roll_call_s)
            # Run before 2p
            # How to use crontab

            if time_now_seconds > end_time_roll_call_s:
                from_time_roll_call_s += 86400
                end_time_roll_call_s += 86400
                print("time_now_seconds > end_time_roll_call_s Time sleep: ", from_time_roll_call_s - time_now_seconds - 30)
                time.sleep(from_time_roll_call_s - time_now_seconds - 30)
            if time_now_seconds < from_time_roll_call_s:
                print("time_now_seconds < from_time_roll_call_s Time sleep: ", from_time_roll_call_s - time_now_seconds)
                time.sleep(from_time_roll_call_s - time_now_seconds)
            if (time_now_seconds >= from_time_roll_call_s) and (time_now_seconds <= end_time_roll_call_s):
                # t = KThread(target=run_roll_call, args=(url_cam, process_stream, process_name, thread_roll_call_manager,True, process_name))
                # t.daemon = True
                # t.start()
                # thread_manager.append(t)

                # Using multiprocess
                try:
                    multiprocessing.set_start_method('spawn')
                except RuntimeError:
                    pass
                # multiprocessing.set_start_method('spawn')
                # boxes, labels, scores, detections_sort = y5_model.predict_sort(frame_rgb, label_select=["head"])
                # RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method
                process = multiprocessing.Process(target=run_roll_call, args=(item_cam, process_stream, process_name,
                                                                              thread_roll_call_manager, end_time_roll_call_s, False))
                process.start()
                process.join()
                process_manager.append(process)
                process.terminate()
                # from_time_roll_call_s += 86400
                # end_time_roll_call_s += 86400
                # print("time sleep after start: ", 86400-30)
                # time.sleep(86400-30)
                process_id = process_dal.find_object_id_by_process_name(process_name)
                data_update = {
                    "status_process": "Stop",
                    "created_at": datetime.now(),
                }
                if len(process_id) > 0:
                    process_dal.update({"_id": process_id[0]["_id"]}, data_update)
                    print("process_name {} Stop".format(process_name))

                break

        options = {"status": True, "status_code": 200, "message": "Start a camera successfully!"}

        return options


@namespace.route("/stop_test/<_id>", methods=["GET"])
class FindById(Resource):
    def get(self, _id):
        """

        :param _id:
        :return:
        """
        global stop
        stop = True

        for p in list_process_stream:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            print("Stop list_process_stream")
        for t in thread_roll_call_manager:
            if t.is_alive():
                t.terminate()
                print("Stop thread_roll_call_manager")
        for t in process_manager:
            if t.is_alive():
                t.terminate()
                print("Stop process_manager")

        # data_update = {
        #     "status_process": "Stop",
        #     "created_at": datetime.now(),
        # }
        #
        # process_name = _id + "_roll_call"
        # process_id = process_dal.find_object_id_by_process_name(process_name)
        # if len(process_id) > 0:
        #     process_dal.update({"_id": process_id[0]["_id"]}, data_update)

        options = {"status": True, "status_code": 200, "message": "Stop a camera successfully!"}

        return options


@namespace.route("/delete_by_name/<name>", methods=["DELETE"])
class FindById(Resource):
    def delete(self, name):
        """Delete an object roll call"""

        list_id = object_dal.find_object_by_name(name)
        list_id = list(map(lambda x: x['_id'], list_id))
        if len(list_id) == 0:
            options = {"message": "object roll call is not found"}
            return options
        object_dal.delete_document(list_id)
        options = {"message": "object roll call is deleted successfully"}
        return options


@namespace.route("/get_all_data", methods=["GET"])
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