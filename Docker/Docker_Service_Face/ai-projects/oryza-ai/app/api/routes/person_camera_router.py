import requests
from fastapi import APIRouter, Depends, HTTPException

from app.api import deps
from app.common.constants.type_camera import TypeCameraEnum
from app.core.config import settings
from app.models import User
from app.schemas.person_camera_schemas import PersonCameraCreate, PersonCameraDelete
from app.services.process_services import service_services, camera_services

router = APIRouter()


@router.post("/create", dependencies=[Depends(deps.get_current_active_admin)])
def create(res: PersonCameraCreate):
    url = settings.SERVER_FACE + "/person_camera/create"
    data = res.dict()
    if res.key_camera == TypeCameraEnum.face_service:
        service_exist = service_services.get(id=res.id_camera)
        if not service_exist:
            raise HTTPException(status_code=400, detail="Service not exist")
        data["host_camera"] = str(service_exist.server.ip_address)
        data["username_camera"] = ""
        data["password_camera"] = ""
        data["port_camera"] = str(service_exist.port)
    else:
        camera_exist = camera_services.get(id=res.id_camera)
        if not camera_exist:
            raise HTTPException(status_code=400, detail="Camera not exist")
        data["host_camera"] = camera_exist.ip_address
        data["username_camera"] = camera_exist.username
        data["password_camera"] = camera_exist.password
        data["port_camera"] = str(camera_exist.port)
    response = requests.post(url, json=data)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.get(
    "/create_multi_camera_user/{person_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
def create_multi_camera_user(
    person_id: str, current_user: User = Depends(deps.get_current_active_admin)
):
    url = settings.SERVER_FACE + "/person_camera/create_multi_camera_user/" + person_id

    cameras = camera_services.get_by_face_ai(company_id=current_user.company.id)
    list_camera = []
    for item in cameras:
        list_camera.append(
            {
                "id_camera": item["id"],
                "key_camera": item["brand_camera"]["key"],
                "host_camera": item["ip_address"],
                "port_camera": str(item["port"]),
                "username_camera": item["username"],
                "password_camera": item["password"],
            }
        )

    response = requests.post(url, json=list_camera)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.get(
    "/create_multi_user_camera/{camera_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
def create_multi_user_camera(
    camera_id: str, current_user: User = Depends(deps.get_current_active_admin)
):
    url = (
        settings.SERVER_FACE
        + "/person_camera/create_multi_user_camera/"
        + str(current_user.company.id)
    )

    camera = camera_services.get_camera(id=camera_id)
    data_send = {
        "id_camera": str(camera.id),
        "key_camera": camera.brand_camera.key,
        "host_camera": camera.ip_address,
        "port_camera": str(camera.port),
        "username_camera": camera.username,
        "password_camera": camera.password,
    }
    response = requests.post(url, json=data_send)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.delete(
    "/delete_multi_user_camera/{camera_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_multi_user_camera(camera_id: str):
    url = settings.SERVER_FACE + "/person_camera/delete_multi_user_camera/" + camera_id

    camera = camera_services.get_camera(id=camera_id)
    data_send = {
        "key_camera": camera.brand_camera.key,
        "host_camera": camera.ip_address,
        "port_camera": str(camera.port),
        "username_camera": camera.username,
        "password_camera": camera.password,
    }
    response = requests.post(url, json=data_send)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.get(
    "/check_create_multi_user_camera/{camera_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
def check_create_multi_user_camera(camera_id: str):
    url = (
        settings.SERVER_FACE
        + "/person_camera/check_create_multi_user_camera/"
        + camera_id
    )
    response = requests.get(url)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.post("/delete/{id}", dependencies=[Depends(deps.get_current_active_admin)])
def delete(id: str, res: PersonCameraDelete):
    url = settings.SERVER_FACE + "/person_camera/delete/" + id
    data = res.dict()
    if res.key_camera == TypeCameraEnum.face_service:
        service_exist = service_services.get(id=res.id_camera)
        if not service_exist:
            raise HTTPException(status_code=400, detail="Service not exist")
        data["host_camera"] = str(service_exist.server.ip_address)
        data["username_camera"] = ""
        data["password_camera"] = ""
        data["port_camera"] = str(service_exist.port)
    else:
        camera_exist = camera_services.get(id=res.id_camera)
        if not camera_exist:
            raise HTTPException(status_code=400, detail="Camera not exist")
        data["host_camera"] = camera_exist.ip_address
        data["username_camera"] = camera_exist.username
        data["password_camera"] = camera_exist.password
        data["port_camera"] = str(camera_exist.port)
    response = requests.post(url, json=data)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail="Delete fail")
    return response.json()


@router.get(
    "/get_by_person_id/{person_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_by_person_id(person_id: str):
    url = settings.SERVER_FACE + "/person_camera/get_by_person_id/" + person_id
    response = requests.get(url)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.get(
    "/get_by_camera_id/{camera_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_by_camera_id(camera_id: str):
    url = settings.SERVER_FACE + "/person_camera/get_by_camera_id/" + camera_id
    response = requests.get(url)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()
