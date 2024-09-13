from fastapi import APIRouter, HTTPException, Request
from app.schemas.process_schemas import (
    StartProcess,
    StopProcess,
    ProcessEnableOut,
    ProcessKillOut,
    Process,
)

from app.common.enum import TypeCameraEnum
from app.services.event_services.hikvision import hik_services
from app.services.event_services.dahua.dahua_event_thread import DahuaEventThread

from app.services.pika_publisher import pika_publisher
from app.common.utils import get_logger

# For testing purposes
from save_file import TestLogger

test_logger = TestLogger()

router = APIRouter()

list_process_hik: dict[str, Process] = {}
list_process_id_hik: dict[str] = {}
list_process_dahua = {}
list_thread_dahua: dict[str, DahuaEventThread] = {}

logger = get_logger("process_logger")
noti_logger = get_logger("noti_logger")


@router.post("/hik/notifications")
async def receive_notification_hik(request: Request):
    """
    This endpoint is open. If camera sends a notification, this server will parse the event, get ip_address,
    if the ip_address is in the list of processes, then send the data to the main server.
    If not, then do nothing.
    """
    body = await request.body()

    # Uncomment this to save the notification to a file
    # with open(f"sample_response/response_{int(time.time())}.txt", "wb") as f:
    #     f.write(body)

    noti_logger.info("Received notification from Hikvision camera")
    try:
        result = hik_services.parse_event(body, list(list_process_hik.keys()))
        if result:
            process = list_process_hik[result["ip_address"]]
            to_send_data = {
                "id": process.process_id,
                "data": {
                    k: result[k]
                    for k in ["user_id", "timestamp", "ip_address", "image_url"]
                },
            }
            to_send_data["data"]["camera_ip"] = to_send_data["data"].pop("ip_address")
            pika_publisher.send_to_rbmq(
                data=to_send_data, exchange_name="FACE_RECOGNITION_EXCHANGES"
            )
            noti_logger.info(f"\nData to send: {to_send_data}\n")
        else:
            noti_logger.debug("Cant parse event")
    except Exception as e:
        noti_logger.debug(f"Error parsing event: {e}")


@router.post("/enable", status_code=201, response_model=ProcessEnableOut)
async def enable_process(
    request: StartProcess,
):
    test_logger.log(f"Enable: {request}")

    if request.brand_camera_key == TypeCameraEnum.hikvision:
        return start_new_process_hik(request)
    elif (
        request.brand_camera_key == TypeCameraEnum.dahua
        or request.brand_camera_key == TypeCameraEnum.access_control
        or request.brand_camera_key == TypeCameraEnum.kbvision
    ):
        return start_new_process_dahua(request, key=request.brand_camera_key)
    else:
        print("Wrong key", request.brand_camera_key)
        raise HTTPException(status_code=400, detail="Wrong key")


@router.post("/kill", status_code=201)
async def kill_process(request: StopProcess):
    test_logger.log(f"Kill: {request}")
    process_id = request.process_id
    process = get_process_hik_by_id(process_id)
    if process is not None:
        return stop_process_hik(process)
    if request.process_id not in list_thread_dahua:
        return ProcessKillOut(process_id=request.process_id, status="not found")
    return stop_process_dahua(request)


@router.get("/get-all", status_code=200)
async def get_all():
    result: dict[str, list[str]] = {}

    # Add Hikvision processes
    for ip_address, process in list_process_hik.items():
        if ip_address not in result:
            result[ip_address] = []
        result[ip_address].append(process.process_id)

    # Add Dahua processes
    for ip_address, process_id in list_process_dahua.items():
        if ip_address not in result:
            result[ip_address] = []
        result[ip_address].append(process_id)

    return result


def get_all_process_status():
    hik = get_hik_process_status()
    dahua = get_dahua_process_status()
    return {**hik, **dahua}


def get_hik_process_status():
    """Get the list of Hikvision processes with their status."""
    list_alive = {}
    for process in list_process_hik.values():
        list_alive[process.process_id] = hik_services.check_alive(process)
    return list_alive


def get_dahua_process_status():
    """Get the list of Dahua processes with their status."""
    list_alive = {}
    threads = get_running_dahua_threads()
    for thread in threads:
        list_alive[thread.process_id] = thread.is_alive()
    return list_alive


def get_process_hik_by_id(process_id: str) -> Process | None:
    for process in list_process_hik.values():
        if process.process_id == process_id:
            return process
    return None


def get_ip_address_by_process_id(process_id: str):
    """For Dahua cameras"""
    for ip_address in list_process_dahua:
        if list_process_dahua[ip_address] == process_id:
            return ip_address


def start_new_process_hik(request: StartProcess) -> ProcessEnableOut:
    """
    Start nothing.
    Just add this server ip address to the camera notification channel.
    Then add the process to the list of processes.
    If event is capture, the this server will send back the result with the process_id
    back to the main server.
    """
    if request.process_id in list_process_id_hik:
        return ProcessEnableOut(
            process_id=request.process_id,
            status="already",
            pid=request.process_id,
        )
    new_process = Process(**request.model_dump())
    if hik_services.start_new_process(new_process):
        list_process_hik[request.ip_address] = new_process
        list_process_id_hik[request.process_id] = request.process_id
        print(f"Process {new_process.process_id} started and added to list_process_hik")
        return ProcessEnableOut(
            process_id=new_process.process_id,
            status="started",
            pid=str(new_process.process_id),
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to start process")


def stop_process_hik(process: Process):
    del list_process_hik[process.ip_address]
    del list_process_id_hik[process.process_id]
    print(f"Process {process.process_id} stopped and removed from list_process_hik")
    if hik_services.stop_process(process):
        return ProcessKillOut(
            process_id=process.process_id,
            status="stopped",
        )
    else:
        raise HTTPException(status_code=500, detail="Failed to stop process")


def get_running_dahua_threads() -> list[DahuaEventThread]:
    return list(list_thread_dahua.values())


def start_new_process_dahua(request: StartProcess, key: str):
    from app.services.event_services.dahua.face_recognition import FaceRecognition
    from app.services.event_services.dahua.access_control import AccessControl
    from app.services.event_services.dahua.traffic_intelligent import TrafficIntelligent

    process_id = request.process_id
    device = None
    if key == TypeCameraEnum.dahua:
        device = FaceRecognition(config=request.model_dump())
    elif key == TypeCameraEnum.access_control:
        device = AccessControl(config=request.model_dump())
    elif key == TypeCameraEnum.kbvision:
        device = TrafficIntelligent(config=request.model_dump())

    # Get the camera configuration
    dahua_cfg = {
        "address": request.ip_address,
        "port": request.port,
        "username": request.username,
        "password": request.password,
        "process_id": process_id,
        "device": device,
    }

    if (
        process_id
        and list_thread_dahua
        and process_id in list_thread_dahua
        and list_thread_dahua[process_id].is_alive()
    ):
        return ProcessEnableOut(
            process_id=process_id,
            status="already",
            pid=str(list_thread_dahua[process_id].ident),
        )
    list_thread_dahua[process_id] = DahuaEventThread(dahua_cfg)

    list_thread_dahua[process_id].start()
    logger.info(f"Process {process_id} started")

    # Save dict of process_id and ip_address
    list_process_dahua[request.ip_address] = process_id

    return ProcessEnableOut(
        process_id=process_id,
        status="started",
        pid=str(list_thread_dahua[process_id].ident),
    )


def stop_process_dahua(request: StopProcess):
    process_id = request.process_id
    if process_id not in list_thread_dahua:
        return ProcessKillOut(process_id=process_id, status="not found")
    dahua_thread = list_thread_dahua[request.process_id]
    dahua_thread.stop()
    if list_thread_dahua[process_id].is_alive():
        raise HTTPException(
            status_code=500, detail=f"Failed to stop process {process_id}"
        )
    del list_thread_dahua[process_id]
    ip_address = get_ip_address_by_process_id(process_id)
    del list_process_dahua[ip_address]
    logger.info(f"Process {process_id} stopped")
    return ProcessKillOut(process_id=process_id, status="stopped")
