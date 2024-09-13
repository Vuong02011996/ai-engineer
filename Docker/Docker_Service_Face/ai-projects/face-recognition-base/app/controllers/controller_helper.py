import subprocess
import cv2
import numpy as np
import time
from glob import glob
import os
# from moviepy.editor import *
# from app.app_utils.minio_utils import upload_image, upload_video
from app.app_utils.file_io_untils import upload_video_from_disk_server_and_get_link, \
    upload_img_from_disk_server_and_get_link

from app.mongo_dal.identity_dal import IdentityDAL
from app.mongo_dal.object_dal.object_safe_region_dal import ObjectSafeRegionDAL
from app.mongo_dal.object_dal.object_sleepless_dal import ObjectSleeplessDAL
from app.mongo_dal.process_dal.process_sleepless_dal import ProcessSleeplessDAL
from app.mongo_dal.camera_dal import CameraDAL

identity_dal = IdentityDAL()
process_dal = ProcessSleeplessDAL()
camera_dal = CameraDAL()
object_safe_region_dal = ObjectSafeRegionDAL()
object_sleepless_dal = ObjectSleeplessDAL()

# define suitable (Codec,CRF,preset) FFmpeg parameters for writer
output_params = {"-vcodec":"libx264", "-crf": 0, "-preset": "fast"}


def create_process_stream(url_cam, url_stream_server, stream=True):
    cap = cv2.VideoCapture(url_cam)
    # command and params for ffmpeg
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if stream is False:
        return None, fps, width, height
    command = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', "{}x{}".format(width, height),
               '-r', str(fps),
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               url_stream_server]
    # ffmpeg -re -i INPUT_FILE_NAME -c copy -f flv rtmp://localhost/live/STREAM_NAME
    # using subprocess and pipe to fetch frame data
    process_stream = subprocess.Popen(command, stdin=subprocess.PIPE, preexec_fn=os.setsid)
    return process_stream, fps, width, height


def find_info_cam_from_process_name(process_dal, process_name):
    camera_id = process_dal.find_camera_by_process_name(process_name)[0]["camera"]
    item_cam = camera_dal.find_by_id(camera_id)
    return item_cam


def get_object_info_safe_region(item, list_name_remain, list_user_id_search=None):
    """

    :param item:
    :param list_name_remain:
    :return:
     {
        "name_object": "Vuong test",
        "url_face_match": "url"
        "url_face": "url",
        "identity": identity,
        "user_id": user_id,
        "time_go_in_safe_region": "2022-01-06 15:56:39.774000",
        "name_region": "Vung 1",
        "image_url": "url",
        "clip_url": ""url",
        "message": "Bé đã vào vùng an toàn quá 10s"
    },
    """
    # Get clip and image url
    data_process = process_dal.find_data_process_by_process_name(item.get("process_name"))[0]
    fps_cam = data_process["fps_cam"]
    url_cam = data_process["url_cam"]
    from_frame = item["from_frame"]
    # if item.get("to_frame") is None:
    #     return None
    # to_frame = item["to_frame"]
    #
    # duration_frame = to_frame - from_frame
    # if duration_frame / fps_cam > 10:
    #     image_url, clip_url = get_image_url_video_url(url_cam, from_frame, to_frame, str(item["_id"]),
    #                                                   item["identity_name"])
    # else:
    #     image_url = clip_url = None

    if item.get("save_status") is not None and item["save_status"] == "stop_save":
        folder_frame_track = item["folder_frame_track"]
        clip_url, list_image_url = get_list_image_url_and_clip_url(item, object_safe_region_dal, folder_frame_track)
    else:
        return None

    if item.get("identity_name") is not None and item["identity_name"] not in list_name_remain:
        # Search user_id from id identity
        user_id = identity_dal.find_by_id(item["identity"])["user_id"]
        if list_user_id_search is not None:
            if user_id in list_user_id_search:
                time_go_in_safe_region = get_utc_time_from_datetime(item["created_at"])
                item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
                object_info = {
                    "id": str(item["_id"]),
                    "name_object": item["identity_name"],
                    "identity": str(item["identity"]),
                    "user_id": user_id,
                    "branch_cam": item_cam["branch_cam"],
                    "class_cam": item_cam["class_cam"],
                    "name_cam": item_cam["name_cam"],
                    "url_face_match": item["avatars_match"],
                    "url_face": [item["avatars"]],
                    "time_go_in_safe_region": time_go_in_safe_region,
                    "name_region": "Vung 1",
                    "image_url": list_image_url,
                    "clip_url": clip_url,
                    "message": "Bé đã vào vùng an toàn quá 10s"
                }
            else:
                object_info = None
        else:
            time_go_in_safe_region = get_utc_time_from_datetime(item["created_at"])
            item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])

            object_info = {
                "id": str(item["_id"]),
                "name_object": item["identity_name"],
                "identity": str(item["identity"]),
                "user_id": user_id,
                "branch_cam": item_cam["branch_cam"],
                "class_cam": item_cam["class_cam"],
                "name_cam": item_cam["name_cam"],
                "url_face_match": item["avatars_match"],
                "url_face": [item["avatars"]],
                "time_go_in_safe_region": time_go_in_safe_region,
                "name_region": "Vung 1",
                "image_url": list_image_url,
                "clip_url": clip_url,
                "message": "Bé đã vào vùng an toàn quá 10s"
            }
            list_name_remain.append(item["identity_name"])
    else:
        if list_user_id_search is None:
            time_go_in_safe_region = get_utc_time_from_datetime(item["created_at"])
            item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
            object_info = {
                "id": str(item["_id"]),
                "name_object": "Unknown",
                "identity": None,
                "user_id": None,
                "branch_cam": item_cam["branch_cam"],
                "class_cam": item_cam["class_cam"],
                "name_cam": item_cam["name_cam"],
                "url_face": [item["avatars"]],
                "url_face_match": None,
                "time_go_in_safe_region": time_go_in_safe_region,
                "name_region": "Vung 1",
                "image_url": list_image_url,
                "clip_url": clip_url,
                "message": "Bé đã vào vùng an toàn quá 10s"
            }
        else:
            object_info = None

    return object_info


def get_object_info_sleepless(item, list_process_name_remain):
    """

    :param item:
    :param list_name_remain:
    :return:
     {
        "time_sleepless": "2022-01-06 15:56:39.774000",
        "name_behavior": Tran troc",
        "image_url": "url",
        "clip_url": ""url",
        "message": "Trằn trọc khó ngủ"
    },
    """

    time_sleepless = get_utc_time_from_datetime(item["created_at"])
    item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
    folder_frame_sleepless = item["folder_frame_region_sleepless"]
    clip_url, list_image_url = get_list_image_url_and_clip_url(item, object_sleepless_dal, folder_frame_sleepless)
    if item.get("identity") is not None:
        st_data = identity_dal.find_by_id(item["identity"])
        name_st = st_data["name"]
        user_id = st_data["user_id"]
        avatar_url = st_data["matching_face_ids"][0]["url_face"]
    else:
        name_st = None
        user_id = None
        avatar_url = None

    if item["process_name"] in list_process_name_remain:
        object_info = {
            "id": str(item["_id"]),
            "branch_cam": item_cam["branch_cam"],
            "class_cam": item_cam["class_cam"],
            "branch_id": item_cam["branch_id"],
            "class_id": item_cam["class_id"],
            "name_cam": item_cam["name_cam"],
            "process_name": item["process_name"],
            "name_behavior": "Trằn trọc khó ngủ",
            "time_sleepless": time_sleepless,
            "region": item["region"],
            "image_url": list_image_url,
            "clip_url": [clip_url],
            "name_st": name_st,
            "user_id": user_id,
            "avatar_url": avatar_url,
            "message": "Cam {} có bé trằn trọc khó ngủ lúc {}".format(item_cam["name_cam"], item["created_at"].strftime("%H:%M:%S %d-%m-%Y"))
        }
        return True, object_info, clip_url
    else:
        object_info = {
            "id": str(item["_id"]),
            "branch_cam": item_cam["branch_cam"],
            "class_cam": item_cam["class_cam"],
            "branch_id": item_cam["branch_id"],
            "class_id": item_cam["class_id"],
            "name_cam": item_cam["name_cam"],
            "process_name": item["process_name"],
            "name_behavior": "Trằn trọc khó ngủ",
            "time_sleepless": time_sleepless,
            "region": item["region"],
            "image_url": list_image_url,
            "clip_url": [clip_url],
            "name_st": name_st,
            "user_id": user_id,
            "avatar_url": avatar_url,
            "message": "Cam {} có bé trằn trọc khó ngủ lúc {}".format(item_cam["name_cam"],
                                                                      item["created_at"].strftime("%H:%M:%S %d-%m-%Y"))
        }
        list_process_name_remain.append(item["process_name"])
        return False, object_info, clip_url


def get_object_sleepless_month(item):
    time_sleepless = get_utc_time_from_datetime(item["created_at"])
    item_cam = find_info_cam_from_process_name(process_dal, item["process_name"])
    hs_data = identity_dal.find_by_id(item["identity"]) if item.get("identity") is not None else {}
    branch_name = None if hs_data.get("branch_name") is None else hs_data["branch_name"]
    class_name = None if hs_data.get("class_name") is None else hs_data["class_name"]
    user_id = hs_data["user_id"] if hs_data.get("user_id") is not None else None

    folder_frame_sleepless = item["folder_frame_region_sleepless"]
    clip_url, list_image_url = get_list_image_url_and_clip_url(item, object_sleepless_dal, folder_frame_sleepless)

    object_info = {
        "id": str(item["_id"]),
        "name_object": item["identity_name"] if item.get("identity_name") is not None else None,
        "identity": str(item["identity"]) if item.get("identity_name") is not None else None,
        "user_id": user_id,
        "branch_name": branch_name,
        "class_name": class_name,
        "name_cam": item_cam["name_cam"],
        "branch_cam": item_cam["branch_cam"],
        "branch_id": item_cam["branch_id"],
        "class_id": item_cam["class_id"],
        "class_cam": item_cam["class_cam"],
        "image_url": list_image_url,
        "clip_url": [clip_url, clip_url],
        "time_sleepless": [time_sleepless],
        "num_day": len([time_sleepless]),
    }
    return object_info


def list_images_to_video_cv2(video_name, list_image):
    frame = cv2.imread(list_image[0])
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name,
                            cv2.VideoWriter_fourcc(*'vp80'),  # X264, MJPG, MPEG, 'vp80', MP4V
                            25, (width, height))
    for image in list_image:
        img = cv2.imread(image)
        video.write(img)
    video.release()


def get_list_image_url_and_clip_url(item, object_dal, folder_frame):

    list_image = glob(folder_frame + "/*.png")
    list_image.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))

    # clip url
    if item.get("clip_url") is None:
        start_time = time.time()
        video_name = folder_frame + '/video_cv2.webm'
        if os.path.exists(video_name) is False:
            list_images_to_video_cv2(video_name, list_image)
        print("list_images_to_video_cv2 cost : ", time.time() - start_time)
        clip_url = upload_video_from_disk_server_and_get_link(video_name)
        #  Update object info to mongDB
        objects_data_elem = {
            "clip_url": clip_url,
            # "created_at": datetime.datetime.now(),
        }
        object_dal.update_document([item["_id"]], [objects_data_elem])
    else:
        clip_url = item["clip_url"]

    # image url
    if item.get("image_url") is None:
        image_url = upload_img_from_disk_server_and_get_link(list_image[0])
        objects_data_elem = {
            "image_url": image_url,
            # "created_at": datetime.datetime.now(),
        }
        object_dal.update_document([item["_id"]], [objects_data_elem])
    else:
        image_url = item["image_url"]

    list_image_url = [image_url]
    return clip_url, list_image_url


def check_save_video():
    folder_frame = "/media/vuong/AI1/Data_clover/Image/test_video/Sleepless_Region_0"
    video_name = folder_frame + '/video_cv2.webm'
    list_image = glob(folder_frame + "/*.png")
    list_image.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    start_time = time.time()
    list_images_to_video_cv2(video_name, list_image)
    print("image to video cost : ", time.time() - start_time)
    clip_url = upload_video_from_disk_server_and_get_link(video_name)
    print(clip_url)


if __name__ == '__main__':
    check_save_video()
