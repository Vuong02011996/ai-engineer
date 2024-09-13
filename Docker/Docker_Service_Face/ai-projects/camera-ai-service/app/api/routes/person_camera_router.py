import threading

from fastapi import APIRouter, HTTPException

from app.common.check_sync_multi_camera import CheckSyncMultiCamera
from app.schemas.person_camera_schemas import (
    PersonCameraCreateDTO,
    PersonCameraDelete,
    PersonCameraCreateMultiCameraUser,
)
from app.services.person_camera_services import person_camera_services

router = APIRouter()


@router.post("/create")
def create(res: PersonCameraCreateDTO):
    checkSyncMultiCamera = CheckSyncMultiCamera()
    status = checkSyncMultiCamera.get_sync_multi_camera(res.id_camera)
    if status and status["status"]:
        raise HTTPException(status_code=400, detail="Camera is being used")
    return person_camera_services.create_user_camera(res)


@router.post("/create_multi_camera_user/{person_id}")
def create_multi_camera_user(
    person_id: str, cameras: list[PersonCameraCreateMultiCameraUser]
):
    return person_camera_services.create_multi_camera_user(
        person_id=person_id, cameras=cameras
    )
    # id_send = uuid.uuid4().hex
    # threading.Thread(target=person_camera_services.create_multi_camera_user,
    #                  args=(id_company, person_id, True, id_socket)).start()
    # return {"id_send": id_socket}


@router.post("/create_multi_user_camera/{id_company}")
def create_multi_user_camera(
    id_company: str, camera: PersonCameraCreateMultiCameraUser
):
    checkSyncMultiCamera = CheckSyncMultiCamera()
    checkSyncMultiCamera.set_sync_multi_camera(camera.id_camera, True, "create")
    # print("create_multi_user_camera",camera.id_camera)
    # return person_camera_services.create_multi_user_camera(id_company=id_company,camera=camera)
    threading.Thread(
        target=person_camera_services.create_multi_user_camera,
        args=(id_company, camera),
    ).start()
    return True


@router.post("/delete_multi_user_camera/{camera_id}")
def delete_multi_user_camera(camera_id: str, res: PersonCameraDelete):
    # return person_camera_services.delete_multi_user_camera(camera_id=camera_id,cameras=cameras)
    checkSyncMultiCamera = CheckSyncMultiCamera()
    checkSyncMultiCamera.set_sync_multi_camera(camera_id, True, "delete")
    threading.Thread(
        target=person_camera_services.delete_multi_user_camera, args=(camera_id, res)
    ).start()
    return True


@router.get("/check_create_multi_user_camera/{camera_id}")
def check_create_multi_user_camera(camera_id: str):
    checkSyncMultiCamera = CheckSyncMultiCamera()
    print("check_create_multi_user_camera", camera_id)

    return checkSyncMultiCamera.get_sync_multi_camera(camera_id)


@router.post("/delete/{id}")
def delete(id: str, res: PersonCameraDelete):
    return person_camera_services.delete(id=id, res=res)


@router.get("/get_by_person_id/{person_id}")
def get_by_person_id(person_id: str):
    return person_camera_services.get_by_person_id(person_id=person_id)


@router.get("/get_by_camera_id/{camera_id}")
def get_by_camera_id(camera_id: str):
    return person_camera_services.get_by_camera_id(camera_id=camera_id)
