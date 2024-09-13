import numpy as np

from app.app_utils.file_io_untils import upload_img_from_disk
from app.controllers.controller_helper import find_info_cam_from_process_name
from app.mongo_dal.process_dal.process_attendance_dal import ProcessAttendanceDAL
from app.mongo_dal.camera_dal import CameraDAL
from app.mongo_dal.identity_dal import IdentityDAL
from app.services.services_helper import get_utc_time_from_datetime
camera_dal = CameraDAL()
process_dal = ProcessAttendanceDAL()
identity_dal = IdentityDAL()


def get_config_from_process_name(process_name, width, height):
    process = process_dal.find_camera_by_process_name(process_name)[0]
    job_process = process["job_process"]
    camera_id = process["camera"]
    item_camera = camera_dal.find_by_id(camera_id)
    jobs_cam = item_camera['jobs_cam']
    config = jobs_cam[job_process]

    # Only get region 1
    if job_process == "safe_area_regions":
        coordinates = config[0]["coordinates"]
    elif job_process == "sleepless":
        coordinates = config[0]["coordinates"]
    else:
        coordinates = config["coordinates"]

    # resize coordinates
    if len(coordinates) == 0:
        coordinates = np.array([[0, 0], [width, height],[width, 0],  [0, height]])
    else:
        for i in range(len(coordinates)):
            coordinates[i][0] *= width
            coordinates[i][1] *= height
            coordinates[i] = list(map(int, coordinates[i]))

    return coordinates


def get_coordinates_roll_call_from_process_name(process_name, width, height):
    process = process_dal.find_camera_by_process_name(process_name)[0]
    camera_id = process["camera"]
    item_camera = camera_dal.find_by_id(camera_id)
    # resize coordinates
    if item_camera.get("jobs_cam") is None \
            or item_camera["jobs_cam"].get("roll_call") is None \
            or item_camera["jobs_cam"]["roll_call"].get("coordinates") is None \
            or len(item_camera["jobs_cam"]["roll_call"]["coordinates"]) == 0:
        coordinates = None
    else:
        coordinates = item_camera["jobs_cam"]["roll_call"]["coordinates"]
        for i in range(len(coordinates)):
            coordinates[i][0] *= width
            coordinates[i][1] *= height
            coordinates[i] = list(map(int, coordinates[i]))

    return coordinates


def get_object_info_roll_call(item, list_name_remain, list_user_id_search=None):
    if item.get("identity_name") is not None and item["identity_name"] not in list_name_remain:
        # Search user_id from id identity
        hs_data = identity_dal.find_by_id(item["identity"])
        # Nếu học sinh nhận diện không có trong hồ sơ đối tượng (database identity bị xóa)
        if hs_data is None:
            return None
        try:
            branch_name = hs_data["branch_name"]
            class_name = hs_data["class_name"]
        except Exception as e:
            print(e)
            branch_name = None,
            class_name = None
        # class_name = hs_data["class_name"]
        user_id = hs_data["user_id"]
        if list_user_id_search is not None:
            if user_id in list_user_id_search:
                time_go_in_class = get_utc_time_from_datetime(item["created_at"])
                item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
                object_info = {
                    "id": str(item["_id"]),
                    "name_object": item["identity_name"],
                    "identity": str(item["identity"]),
                    "user_id": user_id,
                    "branch_cam": branch_name,
                    "class_cam": class_name,
                    "name_cam": item_cam["name_cam"],
                    "url_face_match": item["avatars_match"],
                    "url_face": [item["avatars"], item["avatars_ori"]],
                    # "url_face": [item["avatars"]],
                    "time_go_in_class": time_go_in_class,
                    "time_go_out_class": time_go_in_class,
                }
            else:
                object_info = None
        else:
            time_go_in_class = get_utc_time_from_datetime(item["created_at"])
            item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])

            object_info = {
                "id": str(item["_id"]),
                "name_object": item["identity_name"],
                "identity": str(item["identity"]),
                "user_id": user_id,
                "branch_cam": branch_name,
                "class_cam": class_name,
                "name_cam": item_cam["name_cam"],
                "url_face_match": item["avatars_match"],
                # "url_face": [item["avatars"]],
                "url_face": [item["avatars"], item["avatars_ori"]],
                "time_go_in_class": time_go_in_class,
                "time_go_out_class": time_go_in_class,
            }
            list_name_remain.append(item["identity_name"])
    else:
            object_info = None

    return object_info


def get_object_roll_call_date(item):
    time_go_in_class = get_utc_time_from_datetime(item["created_at"])
    item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
    hs_data = identity_dal.find_by_id(item["identity"])
    if hs_data is None:
        print(item["identity_name"])
        a = 0
        return None
    branch_name = hs_data["branch_name"] if "branch_name" in hs_data else None
    class_name = hs_data["class_name"] if "class_name" in hs_data else None
    user_id = hs_data["user_id"] if "user_id" in hs_data else None
    object_info = {
        "id": str(item["_id"]),
        "name_object": item["identity_name"],
        "identity": str(item["identity"]),
        "user_id": user_id,
        "branch_cam": branch_name,
        "class_cam": class_name,
        "name_cam": item_cam["name_cam"],
        "url_face_match": item["avatars_match"],
        "url_face": [item["avatars"]],
        "time_go_in_class": time_go_in_class,
    }
    return object_info


def get_object_roll_call_name(item, list_name_remain):
    time_go_in_class = get_utc_time_from_datetime(item["created_at"])
    item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
    # Search user_id from id identity
    hs_data = identity_dal.find_by_id(item["identity"])
    if hs_data is None:
        return False, None
    branch_name = hs_data["branch_name"] if "branch_name" in hs_data else None
    class_name = hs_data["class_name"] if "class_name" in hs_data else None
    user_id = hs_data["user_id"] if "user_id" in hs_data else None

    if user_id in list_name_remain:
        object_info = {
            "id": str(item["_id"]),
            "name_object": item["identity_name"],
            "identity": str(item["identity"]),
            "user_id": user_id,
            "branch_cam": branch_name,
            "class_cam": class_name,
            "name_cam": item_cam["name_cam"],
            "url_face_match": [item["avatars_match"]],
            # "url_face": [item["avatars"], item["avatars"]],
            "url_face": [item["avatars"]],
            "time_go_in_class": [time_go_in_class],
            "count_roll_call": 1
        }
        return True, object_info
    else:
        object_info = {
            "id": str(item["_id"]),
            "name_object": item["identity_name"],
            "identity": str(item["identity"]),
            "user_id": user_id,
            "branch_cam": branch_name,
            "class_cam": class_name,
            "name_cam": item_cam["name_cam"],
            "url_face_match": [item["avatars_match"]],
            # "url_face": [item["avatars"], item["avatars"]],
            "url_face": [item["avatars"]],
            "time_go_in_class": [time_go_in_class],
            "count_roll_call": 1
        }
        list_name_remain.append(user_id)
        return False, object_info
