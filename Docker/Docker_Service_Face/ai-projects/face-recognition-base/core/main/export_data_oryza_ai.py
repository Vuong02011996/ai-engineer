"""
Version2: Only save track have face và nhận diện ra tên.
+ Dùng để giảm dung lượng file lưu phía BE.
+ Xét len mảng matching_info > 0 và có phần tử khác Unknown thì sẽ lưu , nếu đã lưu rồi thì chỉ update lại khoảng cách
nếu khoảng cách nhỏ hơn khoảng cách trước đó đã lưu.
"""
import traceback
import numpy as np
import cv2
import json
import base64
import os
from datetime import datetime
import requests
import time
import socket

from Test.align_face_Linh import FaceAligner
# from app.app_utils.minio_utils import upload_image
from app.app_utils.file_io_untils import upload_img_from_disk, ip_run_service_ai
from app.minio_dal.minio_client import upload_array_image_to_minio
from app.mongo_dal.identity_dal import IdentityDAL
from app.milvus_dal.clover_dal import MilvusCloverDAL
from app.mongo_dal.process_dal.process_attendance_dal import ProcessAttendanceDAL
from app.services.services_helper import get_users_and_sent_notify
from app.services.video_offline_face_detection.video_offline_helper import sent_data_with_rabbit_mq
from core.main.main_utils.box_utils import extend_bbox, extend_bbox_percent
from core.main.main_utils.draw import draw_region, draw_boxes_tracking, draw_boxes_one_track_id, draw_box_and_landmark, \
    draw_box_and_landmark_one_box
from core.main.main_utils.helper import get_url_image_person_from_box_head, get_url_image_from_frame_rgb, \
    convert_np_array_to_base64, align_face, align_face_anyshape
import pika
from sentry_sdk import capture_message

#
# from connect_db import connect_socket
#
# client_socket = connect_socket()


# SOCKET_HOST = "192.168.111.63"
# SOCKET_PORT = 1111

# client_socket.connect((os.getenv("SOCKET_HOST"), int(os.getenv("SOCKET_PORT"))))

identity_dal = IdentityDAL()
milvus_staging_dal = MilvusCloverDAL()
process_dal = ProcessAttendanceDAL()


objects_attendance = os.getenv("objects_attendance")
objects_safe_region = os.getenv("objects_safe_region")
url_in_out_roll_call = os.getenv("url_in_out_roll_call")

FACE_RECOGNITION_EXCHANGES = "FACE_RECOGNITION_EXCHANGES"
VIDEO_ANALYZE_FACE_EXCHANGES = "VIDEO_ANALYZE_FACE_EXCHANGES"
VIDEO_ANALYZE_FACE_PROGRESS_EXCHANGES = "VIDEO_ANALYZE_FACE_PROGRESS_EXCHANGES"


def convert_image_face_to_base64(box, frame_ori):
    box = list(map(int, box))
    image_face = frame_ori[box[1]:box[3], box[0]:box[2]]
    try:
        image_face = cv2.cvtColor(image_face, cv2.COLOR_BGR2RGB)
    except Exception as e:
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        print("Lỗi image_face", e)
        return "image face is null", "image face is null"
    _, im_arr = cv2.imencode(".{0}".format('jpg'.lower()), image_face)
    image_bytes = image_face.tobytes()

    # Encode bytes to Base64
    base64_encoded = base64.b64encode(image_bytes).decode('utf-8')

    return base64_encoded


def get_avatar_url(box, frame_ori, frame_count, track_id, name_process):
    box = list(map(int, box))
    image_face = frame_ori[box[1]:box[3], box[0]:box[2]]
    try:
        image_face = cv2.cvtColor(image_face, cv2.COLOR_BGR2RGB)
    except Exception as e:
        capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
        print("Lỗi image_face", e)
        return "image face is null", "image face is null"
    image_name = name_process + "_frame" + str(frame_count) + "_track_" + str(
        track_id)
    avatar_url_ori = upload_img_from_disk(image_name, image_face)

    # extend bounding box for FE
    box_extend = extend_bbox(box, frame_ori.shape, ext_w=20, ext_h=20)
    image_face_extend = frame_ori[box_extend[1]:box_extend[3], box_extend[0]:box_extend[2]]
    image_face_extend = cv2.resize(image_face_extend, (500, 500))
    image_face_extend = cv2.cvtColor(image_face_extend, cv2.COLOR_BGR2RGB)
    image_name = name_process + "_frame" + str(frame_count) + "_track_" + str(
        track_id) + "_extend"
    avatar_url_extend = upload_img_from_disk(image_name, image_face_extend)

    return avatar_url_extend, avatar_url_ori


def export_data_all_face_high_confidence(cam, database_queue, object_dal, info_cam_running):
    """
    Logic : Chỗ ni dùng cho chức năng điểm danh, chỉ đơn giản track id nhận diện ra đối tượng thì lưu vào DB.
    :param cam:
    :param database_queue:
    :param object_dal:
    :return:
    """
    list_name_notify = []
    list_track_id_send = []
    while cam.cap.isOpened():
        track_bbs_ids, matching_info, frame_count, frame_, boxes_face, landmarks_face = database_queue.get()
        frame_rgb = frame_.copy()
        track_ids = track_bbs_ids[:, -1]

        # Kiểm tra có track, head
        if len(matching_info) > 0:
            # tạo ra một danh sách list_name chứa giá trị của khóa 'name' từ mỗi từ điển trong danh sách matching_info
            # không có khóa 'name', giá trị None sẽ được thêm vào danh sách list_name tại vị trí tương ứng.
            list_name = list(map(lambda i: i.get('name', None), matching_info))
            # Kiểm tra có khuôn mặt nhận ra tên thì xử lí
            # if list_name.count("Unknown") != len(list_name):
            list_id = []
            data_update = []
            data_insert = []
            send_first = False
            for idx_box in range(len(list_name)):
                track_id = track_ids[idx_box]
                if np.sum(boxes_face[idx_box]) == 0:
                    continue
                else:
                    a = 0

                if list_name[idx_box] != "Unknown":
                    print("frame_count Unknown: ", frame_count)
                    # Nếu frame đó có ai nhận diện thì không gửi khuôn mặt add nhanh
                    # Nếu không sẽ gửi ảnh không rõ khuôn mặt ở phần else
                    send_first = True
                    # avatar_url_extend, avatar_url_ori = get_avatar_url(boxes_face[idx_box], frame_rgb, frame_count,
                    #                                                    track_id,
                    #                                                    cam.process_name)

                    object_id = object_dal.find_object_id_by_track_id(int(track_ids[idx_box]), cam.process_name)
                    # Nếu chưa lưu thì tạo mới
                    if len(object_id) == 0:
                        box = boxes_face[idx_box]
                        box = list(map(int, box))
                        box_extend = extend_bbox_percent(box, frame_rgb.shape, ext_w=0.6, ext_h=0.6)
                        image_face = frame_rgb[box_extend[1]:box_extend[3], box_extend[0]:box_extend[2]]
                        start_time = time.time()

                        # upload image face to minio and get url
                        avatar_url_extend = upload_array_image_to_minio(image_face, bucket="face",
                                                                        folder_name="attendance_test",
                                                                        image_name="test_" + str(frame_count)+ "_track_" + str(
                                                                                    int(track_id)) + str(int(time.mktime(datetime.today().timetuple()))),
                                                                        mode_rgb="RGB")

                        print("Upload file to minio cost: ", time.time() - start_time)
                        # print("matching_info: ", matching_info)

                        objects_data_elem = {
                            "process_name": cam.process_name,
                            "track_id": int(track_id),
                            "avatars": avatar_url_extend,
                            # "avatars_ori": avatar_url_ori,
                            "acc_face": int(boxes_face[idx_box][-1] * 100),
                            "identity": matching_info[idx_box]["identity_id"],
                            "similarity_distance": matching_info[idx_box]["distance"],
                            "avatars_match": matching_info[idx_box]["url_match"],
                            "identity_name": list_name[idx_box],
                            "created_at": datetime.now(),
                        }
                        data_insert.append(objects_data_elem)

                        """3. Bắn data qua oryza AI"""
                        # if list_name[idx_box] not in list_name_notify:
                        # Name not in list
                        is_key_not_present = all(list_name[idx_box] not in d for d in list_name_notify)

                        print("list_name_notify: ", list_name_notify)
                        print("is_key_not_present: ", is_key_not_present)
                        if is_key_not_present:
                            send_data_info = {list_name[idx_box]: frame_count}
                            list_name_notify.append(send_data_info)
                            # sent data to rabbit
                            identity = matching_info[idx_box]["identity_id"]
                            data_student = identity_dal.find_by_id(identity)
                            process_id = process_dal.find_process_id_by_process_name(cam.process_name)
                            print("process_id: ", process_id[0]["process_id"])
                            data_send = {"id": process_id[0]["process_id"],
                                         "data": {
                                             'camera_ip': cam.ip_camera,
                                             'user_id': data_student["user_id"],
                                             # 'timestamp': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                                             'timestamp': int(time.mktime(datetime.today().timetuple())),
                                             'image_url': avatar_url_extend,
                                             'box_face': box_extend
                                         }
                                         }
                            print("data_send: ", data_send)
                            # pikaPublisher = PikaPublisher()
                            sent_data_with_rabbit_mq(data_send, FACE_RECOGNITION_EXCHANGES)
                        else:
                            # If name have in list get frame
                            frame_of_name = next((item[list_name[idx_box]] for item in list_name_notify if
                                                  list_name[idx_box] in item), None)
                            time_sent = frame_count - frame_of_name
                            print("time_sent : ", time_sent)
                            print("5 * cam.fps : ", 10 * cam.fps)
                            if time_sent > 10 * cam.fps:
                                # sent data to rabbit
                                identity = matching_info[idx_box]["identity_id"]
                                data_student = identity_dal.find_by_id(identity)
                                process_id = process_dal.find_process_id_by_process_name(cam.process_name)
                                print("process_id: ", process_id[0]["process_id"])
                                data_send = {"id": process_id[0]["process_id"],
                                             "data": {
                                                 'camera_ip': cam.ip_camera,
                                                 'user_id': data_student["user_id"],
                                                 # 'timestamp': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                                                 'timestamp': int(time.mktime(datetime.today().timetuple())),
                                                 'image_url': avatar_url_extend,
                                                 'box_face': box_extend
                                                }
                                             }
                                print("data_send: ", data_send)
                                # pikaPublisher = PikaPublisher()
                                sent_data_with_rabbit_mq(data_send, FACE_RECOGNITION_EXCHANGES)
                                # update frame count
                                for item in list_name_notify:
                                    if list_name[idx_box] in item:
                                        item[list_name[idx_box]] = frame_count
                                        break
                                print("list_name_notify update: ", list_name_notify)
                            else:
                                print("Don't send")

                    # Nếu có rồi thì và khoảng cách nhỏ hơn thì update khoảng cách
                    elif len(object_id) == 1:
                        if matching_info[idx_box]["distance"] > object_id[0]["similarity_distance"]:
                            #  check if track was exited identity just update when distance < distance before.
                            list_id.append(object_id[0]["_id"])
                            objects_data_elem = {
                                # "avatars": avatar_url_extend,
                                # "avatars_ori": avatar_url_ori,
                                "have_new_face": True,
                                "identity": matching_info[idx_box]["identity_id"],
                                "similarity_distance": matching_info[idx_box]["distance"],
                                "avatars_match": matching_info[idx_box]["url_match"],
                                "identity_name": list_name[idx_box],
                                "created_at": datetime.now(),
                            }
                            data_update.append(objects_data_elem)
                else:
                    """
                    Sent data when face have high confidence
                    [[0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00 0.00000000e+00],
                     [1.58700000e+03 1.87000000e+02 1.61700000e+03 2.30000000e+02 6.50106668e-01], 
                     [5.04000000e+02 7.22000000e+02 5.49000000e+02 7.87000000e+02 6.50106668e-01], 
                     [6.54000000e+02 2.28000000e+02 6.89000000e+02 2.70000000e+02 6.62677228e-01], 
                     [3.92000000e+02 3.31000000e+02 4.31000000e+02 3.79000000e+02 6.62677228e-01], 
                     [4.72000000e+02 4.28000000e+02 5.20000000e+02 4.87000000e+02 6.62677228e-01], 
                     [3.58000000e+02 6.00000000e+02 4.07000000e+02 6.61000000e+02 6.62677228e-01]]
                    """
                    confidence = boxes_face[idx_box][-1]
                    # print("confidence: ", confidence)
                    if confidence > 0.7:  # 0.75
                        # print("frame_count > 0.68: ", frame_count)
                        if send_first is False and track_id not in list_track_id_send:
                            # print("track_id: ", track_id)
                            box = boxes_face[idx_box]
                            box = list(map(int, box))
                            w_face = box[2] - box[0]
                            h_face = box[3] - box[1]
                            if w_face > 30 and h_face > 30:
                                box_extend = extend_bbox_percent(box, frame_rgb.shape, ext_w=0.6, ext_h=0.6)
                                image_face = frame_rgb[box_extend[1]:box_extend[3], box_extend[0]:box_extend[2]]
                                # upload image face to minio and get url
                                avatar_url_extend = upload_array_image_to_minio(image_face, bucket="face",
                                                                                folder_name="attendance_test",
                                                                                image_name=f"face_box_{w_face}_{h_face}_" + str(
                                                                                    frame_count) + "_track_" + str(
                                                                                    track_id),
                                                                                mode_rgb="RGB")
                                print("avatar_url_extend: ", avatar_url_extend)

                                # Align Face
                                # h, w, c = image_face.shape
                                # image_landmark = draw_box_and_landmark_one_box(frame_rgb.copy(), box[0:4], landmark=landmarks_face[idx_box])
                                # image_face_draw_landmark = image_landmark[box_extend[1]:box_extend[3], box_extend[0]:box_extend[2]]
                                # cv2.imwrite(f"/home/oryza/Desktop/test_image/image_landmark_{frame_count}_{idx_box}.png", image_face_draw_landmark)

                                # face_align = FaceAligner(exp_width=w, exp_height=h)
                                # face_align = FaceAligner()
                                # # warped, M, face = face_align.align(frame_rgb, box[0:4], landmarks_face[idx_box], image_size=[w, h])
                                # warped, M, face = face_align.align(frame_rgb, box[0:4], landmarks_face[idx_box])
                                # print("box[0:4]: ", box[0:4])
                                # print("landmarks_face[idx_box]: ", landmarks_face[idx_box])
                                # # image_face_after_align = image_rgb_align[box_extend[1]:box_extend[3],
                                # #                            box_extend[0]:box_extend[2]]
                                # cv2.imwrite(f"/home/oryza/Desktop/test_image/image_landmark_face_align{frame_count}_{idx_box}.png",
                                #             face)
                                # image_face_align = align_face_anyshape(frame_rgb, box[0:4], landmarks_face[idx_box])
                                #
                                # # upload image face to minio and get url
                                # avatar_url_extend_align = upload_array_image_to_minio(image_face_align, bucket="face",
                                #                                                 folder_name="attendance_test",
                                #                                                 image_name="warped_test_" + str(
                                #                                                     frame_count) + "_track_" + str(
                                #                                                     track_id),
                                #                                                 mode_rgb="RGB")
                                # print("avatar_url_extend align: ", avatar_url_extend_align)
                                # print("Upload file to minio cost: ", time.time() - start_time)
                                list_track_id_send.append(track_id)

                                # Send data to RabbitMQ
                                process_id = process_dal.find_process_id_by_process_name(cam.process_name)
                                # print("process_id: ", process_id[0]["process_id"])
                                data_send = {"id": process_id[0]["process_id"],
                                             "data": {
                                                 'camera_ip': cam.ip_camera,
                                                 # 'user_id': data_student["user_id"],
                                                 'timestamp': int(time.mktime(datetime.today().timetuple())),
                                                 'image_url': avatar_url_extend,
                                                 'box_face': box_extend
                                             }
                                             }
                                sent_data_with_rabbit_mq(data_send, FACE_RECOGNITION_EXCHANGES)

                        # Chỉ lấy khuôn mặt khi có confidence lớn hơn ngưỡng đầu tiên trong list
                        # Vì những confidence sau đều giống cái đầu tiên và box face không chính xác
                        send_first = True

            if len(data_update) > 0:
                object_dal.update_document(list_id, data_update)
            if len(data_insert) > 0:
                object_dal.save_document(data_insert)

    cam.cap.release()


def export_data_video_offline_v1(cam, database_queue, object_dal, info_cam_running):
    """
    Logic : Chỗ ni dùng cho chức năng điểm danh, chỉ đơn giản track id nhận diện ra đối tượng thì lưu vào DB.
    :param cam:
    :param database_queue:
    :param object_dal:
    :return:
    """
    list_name_notify = []
    list_track_id_send = []
    while cam.cap.isOpened():
        track_bbs_ids, matching_info, frame_count, frame_, boxes_face, landmarks_face = database_queue.get()
        frame_rgb = frame_.copy()
        track_ids = track_bbs_ids[:, -1]

        # Kiểm tra có track, head
        if len(matching_info) > 0:
            # tạo ra một danh sách list_name chứa giá trị của khóa 'name' từ mỗi từ điển trong danh sách matching_info
            # không có khóa 'name', giá trị None sẽ được thêm vào danh sách list_name tại vị trí tương ứng.
            list_name = list(map(lambda i: i.get('name', None), matching_info))
            # Kiểm tra có khuôn mặt nhận ra tên thì xử lí
            # if list_name.count("Unknown") != len(list_name):
            list_id = []
            data_update = []
            data_insert = []
            send_first = False
            for idx_box in range(len(list_name)):
                track_id = track_ids[idx_box]
                if np.sum(boxes_face[idx_box]) == 0:
                    continue
                else:
                    a = 0

                if list_name[idx_box] != "Unknown":
                    print("frame_count Unknown: ", frame_count)
                    # Nếu frame đó có ai nhận diện thì không gửi khuôn mặt add nhanh
                    # Nếu không sẽ gửi ảnh không rõ khuôn mặt ở phần else
                    send_first = True
                    # avatar_url_extend, avatar_url_ori = get_avatar_url(boxes_face[idx_box], frame_rgb, frame_count,
                    #                                                    track_id,
                    #                                                    cam.process_name)

                    object_id = object_dal.find_object_id_by_track_id(int(track_ids[idx_box]), cam.process_name)
                    # Nếu chưa lưu thì tạo mới
                    if len(object_id) == 0:
                        box = boxes_face[idx_box]
                        box = list(map(int, box))
                        box_extend = extend_bbox_percent(box, frame_rgb.shape, ext_w=0.6, ext_h=0.6)
                        image_face = frame_rgb[box_extend[1]:box_extend[3], box_extend[0]:box_extend[2]]
                        start_time = time.time()

                        # upload image face to minio and get url
                        avatar_url_extend = upload_array_image_to_minio(image_face, bucket="face",
                                                                        folder_name="attendance_test",
                                                                        image_name="test_" + str(frame_count)+ "_track_" + str(
                                                                                    int(track_id)) + str(int(time.mktime(datetime.today().timetuple()))),
                                                                        mode_rgb="RGB")

                        print("Upload file to minio cost: ", time.time() - start_time)
                        # print("matching_info: ", matching_info)

                        objects_data_elem = {
                            "process_name": cam.process_name,
                            "track_id": int(track_id),
                            "avatars": avatar_url_extend,
                            # "avatars_ori": avatar_url_ori,
                            "acc_face": int(boxes_face[idx_box][-1] * 100),
                            "identity": matching_info[idx_box]["identity_id"],
                            "similarity_distance": matching_info[idx_box]["distance"],
                            "avatars_match": matching_info[idx_box]["url_match"],
                            "identity_name": list_name[idx_box],
                            "created_at": datetime.now(),
                        }
                        data_insert.append(objects_data_elem)

                        """3. Bắn data qua oryza AI"""
                        # if list_name[idx_box] not in list_name_notify:
                        # Name not in list
                        is_key_not_present = all(list_name[idx_box] not in d for d in list_name_notify)

                        print("list_name_notify: ", list_name_notify)
                        print("is_key_not_present: ", is_key_not_present)
                        if is_key_not_present:
                            send_data_info = {list_name[idx_box]: frame_count}
                            list_name_notify.append(send_data_info)
                            # sent data to rabbit
                            data_send = {"id": "6698d5869722151addda84f1",
                                         "data": {
                                             'timestamp': int(time.mktime(datetime.today().timetuple())),
                                             'image_url': avatar_url_extend,
                                         }
                                         }
                            sent_data_with_rabbit_mq(data_send, VIDEO_ANALYZE_FACE_EXCHANGES)
                            print("data_send: ", data_send)
                        else:
                            # If name have in list get frame
                            frame_of_name = next((item[list_name[idx_box]] for item in list_name_notify if
                                                  list_name[idx_box] in item), None)
                            time_sent = frame_count - frame_of_name
                            print("time_sent : ", time_sent)
                            print("5 * cam.fps : ", 20 * cam.fps)
                            if time_sent > 20 * cam.fps:
                                # sent data to rabbit
                                data_send = {"id": "6698d5869722151addda84f1",
                                             "data": {
                                                 'timestamp': int(time.mktime(datetime.today().timetuple())),
                                                 'image_url': avatar_url_extend,
                                             }
                                             }
                                sent_data_with_rabbit_mq(data_send, VIDEO_ANALYZE_FACE_EXCHANGES)
                                print("data_send: ", data_send)
                                # update frame count
                                for item in list_name_notify:
                                    if list_name[idx_box] in item:
                                        item[list_name[idx_box]] = frame_count
                                        break
                                print("list_name_notify update: ", list_name_notify)
                            else:
                                print("Don't send")

                    # Nếu có rồi thì và khoảng cách nhỏ hơn thì update khoảng cách
                    elif len(object_id) == 1:
                        if matching_info[idx_box]["distance"] > object_id[0]["similarity_distance"]:
                            #  check if track was exited identity just update when distance < distance before.
                            list_id.append(object_id[0]["_id"])
                            objects_data_elem = {
                                # "avatars": avatar_url_extend,
                                # "avatars_ori": avatar_url_ori,
                                "have_new_face": True,
                                "identity": matching_info[idx_box]["identity_id"],
                                "similarity_distance": matching_info[idx_box]["distance"],
                                "avatars_match": matching_info[idx_box]["url_match"],
                                "identity_name": list_name[idx_box],
                                "created_at": datetime.now(),
                            }
                            data_update.append(objects_data_elem)

            if len(data_update) > 0:
                object_dal.update_document(list_id, data_update)
            if len(data_insert) > 0:
                object_dal.save_document(data_insert)

    cam.cap.release()


def export_data_video_offline(cam, database_queue, object_dal, info_cam_running):
    """
    Logic : Chỗ ni dùng cho chức năng điểm danh, chỉ đơn giản track id nhận diện ra đối tượng thì lưu vào DB.
    :param cam:
    :param database_queue:
    :param object_dal:
    :return:
    """
    while cam.cap.isOpened():
        track_bbs_ids, matching_info, frame_count, frame_, boxes_face, landmarks_face = database_queue.get()
        frame_rgb = frame_.copy()
        track_ids = track_bbs_ids[:, -1]

        # Kiểm tra có track, head
        if len(matching_info) > 0:
            # tạo ra một danh sách list_name chứa giá trị của khóa 'name' từ mỗi từ điển trong danh sách matching_info
            # không có khóa 'name', giá trị None sẽ được thêm vào danh sách list_name tại vị trí tương ứng.
            list_name = list(map(lambda i: i.get('name', None), matching_info))
            # Kiểm tra có khuôn mặt nhận ra tên thì xử lí
            # if list_name.count("Unknown") != len(list_name):
            for idx_box in range(len(list_name)):
                track_id = track_ids[idx_box]
                if np.sum(boxes_face[idx_box]) == 0:
                    continue
                else:
                    a = 0

                if list_name[idx_box] != "Unknown":
                    box = boxes_face[idx_box]
                    box = list(map(int, box))
                    box_extend = extend_bbox_percent(box, frame_rgb.shape, ext_w=0.6, ext_h=0.6)
                    image_face = frame_rgb[box_extend[1]:box_extend[3], box_extend[0]:box_extend[2]]
                    # upload image face to minio and get url
                    avatar_url_extend = upload_array_image_to_minio(image_face, bucket="face",
                                                                    folder_name="attendance_video_offline",
                                                                    image_name=str(frame_count) + "_track_" + str(track_id),
                                                                    mode_rgb="RGB")
                    print("avatar_url_extend: ", avatar_url_extend)
                    data_send = {"id": "6698d5869722151addda84f1",
                                 "data": {
                                     'timestamp': int(time.mktime(datetime.today().timetuple())),
                                     'image_url': avatar_url_extend,
                                 }
                                 }
                    sent_data_with_rabbit_mq(data_send, VIDEO_ANALYZE_FACE_EXCHANGES)
                    print("avatar_url_extend: ", avatar_url_extend)

    cam.cap.release()

