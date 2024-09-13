from app.common.constants.enums import TypeServiceEnum
from app.models import Process, Camera, Service, TypeService, BrandCamera, Server
from app.core.config import settings
from app.common.constants import rabbitmq_constants
from app.services.event_services import type_service_services
from app.services.vms_services import vms_services
from app.services.camera_settings import (
    st_crowd_sv,
    st_item_forgotten_sv,
    st_uniform_sv,
    st_tampering_sv,
    st_camera_traffic_sv,
    st_lane_sv,
)
from app.services import (
    st_leaving_sv,
    st_tripwire_sv,
    st_loitering_sv,
    st_plate_number_sv,
    st_illegal_parking_sv,
)
from fastapi import HTTPException
import cv2


def test_rtsp_connection(rtsp):
    if rtsp == "" or rtsp is None:
        return False
    cap = cv2.VideoCapture(rtsp)
    if not cap.isOpened():
        print("RTSP connection failed: Unable to open stream")
        return False
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("RTSP connection failed: Unable to read frame")
        return False
    print("RTSP connection successful")
    return True


def get_rtsp_vms(camera: Camera):
    id_vms = camera.other_info.get("id_vms", "")
    if id_vms == "":
        print("Get rtsp vms fail, id_vms not found")
        return None
    vms = vms_services.get_by_company_id(company_id=str(camera.company.id))
    address = vms.ip_address.replace("http://", "").replace("https://", "")
    rtsp = f"rtsp://{vms.username}:{vms.password}@{address}:{vms.port}/{id_vms}"
    print(f"Get rtsp vms success, Generated RTSP URL: {rtsp}")
    # Test the rtsps connection
    if test_rtsp_connection(rtsp):
        return rtsp
    else:
        print("Get rtsp vms fail, RTSP connection test failed for VMS")
        return None


def get_rtsp_auth(camera: Camera):
    username = camera.username
    password = camera.password
    if username is not None and password is not None:
        name_pass = f"{username}:{password}@"
        rtsp = camera.rtsp
        if rtsp == "" or rtsp is None:
            print("Get rtsp auth fail: rtsp not found")
            return None
        if name_pass not in rtsp:
            rtsp = rtsp.replace("rtsp://", f"rtsp://{name_pass}")
        print(f"2. Generated RTSP URL with camera auth: {rtsp}")
        return rtsp
    return None


def get_working_rtsp(camera: Camera):
    # print("\nGet rtsp")
    # rtsp = camera.rtsp_vms
    # print("1. Initial rtsp_vms: ", rtsp)
    # # Test the connection
    # if not test_rtsp_connection(rtsp):
    #     print("! rtsp_vms not work, create a new one")
    #     rtsp = get_rtsp_vms(camera)
    #     if not test_rtsp_connection(rtsp):
    #         print("! new created rtsp_vms not work, create a rtsp from camera auth")
    #         rtsp = get_rtsp_auth(camera)
    #         if not test_rtsp_connection(rtsp):
    #             print("! rtsp with camera auth not work, no hope")
    #             return None
    # print("\nFinal RTSP URL: ", rtsp)
    rtsp = get_rtsp_auth(camera)
    return rtsp


def get_payload(process: Process):
    service: Service = process.service
    camera: Camera = process.camera
    server = service.server

    payload = {}
    type_service: TypeService = type_service_services.get_type_service(
        id=process.id_type_service
    )
    if type_service.key == rabbitmq_constants.FACE_RECOGNITION_EXCHANGES:
        print("Processing FACE_RECOGNITION_EXCHANGES")
        payload = get_face_recognition_payload(process, camera, service)
    elif type_service.key == rabbitmq_constants.crowd:
        print("Processing CROWD_DETECTION_EXCHANGES")
        payload = get_crow_detection_payload(process, camera)
    elif type_service.key == rabbitmq_constants.plate_number:
        print("Processing PLATE_NUMBER_EXCHANGES")
        payload = get_plate_number_payload(process, camera, service)
    elif type_service.key == rabbitmq_constants.DETECT_ITEMS_FORGOTTEN_EXCHANGES:
        print("Processing DETECT_ITEMS_FORGOTTEN_EXCHANGES")
        payload = get_item_forgotten_payload(process, camera)
    elif type_service.key == rabbitmq_constants.IDENTIFY_UNIFORMS_EXCHANGES:
        print("Processing IDENTIFY_UNIFORMS_EXCHANGES")
        payload = get_identify_uniform_payload(process, camera, service, server)
    elif type_service.key in [
        rabbitmq_constants.loitering,
        rabbitmq_constants.intrusion,
    ]:
        print(f"Processing {type_service.key}")
        payload = get_loitering_payload(process, camera, type_service.key)
    elif type_service.key == rabbitmq_constants.illegal_parking:
        print("Processing ILLEGAL_PARKING_EXCHANGES")
        payload = get_illegal_parking_payload(process, camera)
    elif type_service.key == rabbitmq_constants.CAMERA_TAMPERING_EXCHANGES:
        print("Processing CAMERA_TAMPERING_EXCHANGES")
        payload = get_tampering_payload(process, camera)
    elif type_service.key == rabbitmq_constants.CAMERA_TRAFFIC_SIGNAL_EXCHANGES:
        print("Processing CAMERA_TRAFFIC_SIGNAL_EXCHANGES")
        payload = get_camera_traffic_payload(process, camera)
    elif type_service.key == rabbitmq_constants.tripwire:
        print("Processing TRIPWIRE_EXCHANGES")
        payload = get_tripwire_payload(process, camera)
    elif type_service.key in [
        rabbitmq_constants.LINE_VIOLATION_EXCHANGES,
        rabbitmq_constants.LANE_VIOLATION_EXCHANGES,
        rabbitmq_constants.WRONG_WAY_EXCHANGES,
    ]:
        print(f"Processing {type_service.key}")
        payload = get_lane_violation_payload(process, camera, type_service.key)
    elif type_service.key == rabbitmq_constants.LEAVING_EXCHANGES:
        print("Processing LEAVING_EXCHANGES")
        payload = get_leaving_payload(process, camera)
    else:
        print(f"Unknown type_service.key: {type_service.key}")

    print("\nGenerated payload: ", payload)
    return payload


def get_face_recognition_payload(process: Process, camera: Camera, service: Service):
    if service.type == TypeServiceEnum.ai_camera:
        brand_camera: BrandCamera = camera.brand_camera
        payload = {
            "process_id": str(process.id),
            "brand_camera_key": brand_camera.key,
            "ip_address": camera.ip_address,
            "port": int(camera.port),
            "username": camera.username,
            "password": camera.password,
        }
    if service.type == TypeServiceEnum.ai_service:
        # rtsp = get_working_rtsp(camera)
        # if rtsp is None:
        #     return None
        rtsp = process.rtsp
        payload = {
            "process_id": str(process.id),
            "rtsp": rtsp,
            "ip_camera": camera.ip_address,
        }
    return payload


def get_crow_detection_payload(process: Process, camera: Camera):
    # rtsp = get_working_rtsp(camera)
    # if rtsp is None:
    #     return None
    rtsp = process.rtsp
    crowd = st_crowd_sv.get_by_id_camera(id_camera=str(camera.id))
    boundary = "[[0,0],[1,0],[1,1],[0,1]]"
    min_human_count = 2
    min_neighbours = 2
    distance_threshold = 2
    waiting_time_to_start_alarm = 2
    waiting_time_for_next_alarm = 2
    if crowd:
        boundary = crowd.boundary
        min_human_count = crowd.min_human_count
        min_neighbours = crowd.min_neighbours
        distance_threshold = crowd.distance_threshold
        waiting_time_to_start_alarm = crowd.waiting_time_to_start_alarm
        waiting_time_for_next_alarm = crowd.waiting_time_for_next_alarm
    payload = {
        "username": camera.username,
        "password": camera.password,
        "address": camera.ip_address,
        "rtsp": rtsp,
        "boundary": boundary,
        "min_human_count": min_human_count,
        "min_neighbours": min_neighbours,
        "distance_threshold": distance_threshold,
        "waiting_time_to_start_alarm": waiting_time_to_start_alarm,
        "waiting_time_for_next_alarm": waiting_time_for_next_alarm,
        "process_id": str(process.id),
    }
    return payload


def get_plate_number_payload(process: Process, camera: Camera, service: Service):
    if service.type == TypeServiceEnum.ai_camera:
        brand_camera: BrandCamera = camera.brand_camera
        payload = {
            "process_id": str(process.id),
            "brand_camera_key": brand_camera.key,
            "ip_address": camera.ip_address,
            "port": int(camera.port),
            "username": camera.username,
            "password": camera.password,
        }
    elif service.type == TypeServiceEnum.ai_service:
        setting_plate = st_plate_number_sv.get_by_camera(str(camera.id))
        rtsp = process.rtsp
        payload = {
            "username": camera.username,
            "password": camera.password,
            "status": True,
            "address": camera.ip_address,
            "ip_host": camera.ip_address,
            "port_host": str(camera.port),
            "rtsp": rtsp,
            "id": str(process.id),
            "object_detect": "plate",
            "line": "[0, 0.5, 1, 0.5]",
        }
        if setting_plate:
            payload["object_detect"] = setting_plate.object_detect
            payload["line"] = setting_plate.line
    return payload


def get_item_forgotten_payload(process: Process, camera: Camera):
    st_difs = st_item_forgotten_sv.get_by_id_camera(id_camera=str(camera.id))
    # rtsp = get_working_rtsp(camera)
    # if rtsp is None:
    #     return None
    rtsp = process.rtsp
    if st_difs:
        boundary = st_difs.boundary
        waiting_time = st_difs.waiting_time
    else:
        boundary = settings.DIFS_BOUNDARY
        waiting_time = settings.DIFS_WAITING_TIME

    payload = {
        "username": camera.username,
        "password": camera.password,
        "address": camera.ip_address,
        "rtsp": rtsp,
        "boundary": boundary,
        "waiting_time": waiting_time,
        "process_id": str(process.id),
    }
    return payload


def get_identify_uniform_payload(
    process: Process, camera: Camera, service: Service, server: Server
):
    from app.services.camera_settings.setting_uniform_company_services import (
        setting_uniform_company_services,
    )

    # rtsp = get_working_rtsp(camera)
    # if rtsp is None:
    #     return None
    rtsp = process.rtsp

    uniform_company_services = setting_uniform_company_services.get_by_id_company(
        id_company=str(camera.company.id)
    )
    if not uniform_company_services:
        return None
    try:
        response2 = setting_uniform_company_services.create_from_sub_service(
            uniform_company_services,
            ip_address=server.ip_address,
            port=service.port,
        )
        if not response2:
            return None
    except Exception as e:
        print(e)
        return None

    st_ius = st_uniform_sv.get_by_id_camera(id_camera=str(camera.id))
    if st_ius:
        boundary = st_ius.boundary
        waiting_time = st_ius.waiting_time
    else:
        boundary = settings.IUS_BOUNDARY
        waiting_time = settings.IUS_WAITING_TIME
    payload = {
        "username": camera.username,
        "password": camera.password,
        "address": camera.ip_address,
        "rtsp": rtsp,
        "process_id": str(process.id),
        "waiting_time": waiting_time,
        "boundary": boundary,
        "company_id": str(camera.company.id),
    }
    return payload


def get_loitering_payload(process: Process, camera: Camera, key_ai: str):
    st_ld = st_loitering_sv.get_by_camera(str(camera.id), key_ai)
    if st_ld:
        boundary = st_ld.boundary
        waiting_time = st_ld.waiting_time
    else:
        raise HTTPException(status_code=400, detail="Setting not found")
    rtsp = process.rtsp
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "boundary": boundary,
        "waiting_time": waiting_time,
    }
    return payload


def get_leaving_payload(process: Process, camera: Camera):
    st_leaving = st_leaving_sv.get_by_camera(str(camera.id))
    if st_leaving:
        area_str = st_leaving.area_str
        object_str = st_leaving.object_str
        image_url = st_leaving.image_url
        alert_delay = st_leaving.alert_delay
        alert_interval = st_leaving.alert_interval
    rtsp = process.rtsp
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "boundary": area_str,
        "object_box": object_str,
        "image_url": image_url,
        "alert_delay": alert_delay,
        "alert_interval": alert_interval,
    }
    return payload


def get_illegal_parking_payload(process: Process, camera: Camera):
    rtsp = process.rtsp
    st_ip = st_illegal_parking_sv.get_by_camera(str(camera.id))
    if st_ip:
        boundary = st_ip.boundary
        waiting_time = st_ip.waiting_time
        alert_interval = st_ip.alert_interval
    else:
        boundary = settings.IP_BOUNDARY
        waiting_time = settings.IP_WAITING_TIME
        alert_interval = settings.IP_ALERT_INTERVAL
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "boundary": boundary,
        "waiting_time": waiting_time,
        "alert_interval": alert_interval,
    }
    return payload


def get_tampering_payload(process: Process, camera: Camera):
    # rtsp = get_working_rtsp(camera)
    # if rtsp is None:
    #     return None
    rtsp = process.rtsp
    setting_tampering = st_tampering_sv.get_by_id_camera(id_camera=str(camera.id))
    if setting_tampering:
        alarm_interval = setting_tampering.alarm_interval
    else:
        alarm_interval = 10
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "alarm_interval": alarm_interval,
    }
    return payload


def get_camera_traffic_payload(process: Process, camera: Camera):
    # rtsp = get_working_rtsp(camera)
    # if rtsp is None:
    #     return None
    rtsp = process.rtsp
    setting_camera_traffic = st_camera_traffic_sv.get_by_id_camera(
        id_camera=str(camera.id)
    )
    if setting_camera_traffic:
        light_boundary = setting_camera_traffic.light_boundary
    else:
        light_boundary = settings.LD_BOUNDARY
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "light_boundary": light_boundary,
    }
    return payload


def get_tripwire_payload(process: Process, camera: Camera):
    rtsp = process.rtsp
    st_tw = st_tripwire_sv.get_by_camera(camera_id=str(camera.id))
    if st_tw:
        line = st_tw.line
    else:
        line = settings.TW_LINE
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "line": line,
    }
    return payload


def get_lane_violation_payload(process: Process, camera: Camera, key_ai: str):
    rtsp = process.rtsp
    st_lv = st_lane_sv.get_by_camera(str(camera.id), key_ai)
    if st_lv:
        lanes = st_lv.lanes
    else:
        raise HTTPException(status_code=400, detail="Setting not found")
    payload = {
        "process_id": str(process.id),
        "ip_camera": camera.ip_address,
        "rtsp": rtsp,
        "lanes": lanes,
    }
    if key_ai == rabbitmq_constants.LANE_VIOLATION_EXCHANGES:
        payload["lane_codes"] = st_lv.codes
    return payload
