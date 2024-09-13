import requests
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.common.utils.image_face import check_one_face
from app.core.config import settings
from app.services.camera_services import camera_services
from app.services.process_services import service_services


router = APIRouter()


@router.patch("/create/{id_person}")
async def create_image_by_person(id_person: str, files: UploadFile = File(...)):
    url = settings.SERVER_FACE + "/person_image/create/" + id_person
    files_to_send = []
    file_content = await files.read()
    files_to_send.append(("files", (files.filename, file_content, files.content_type)))
    response = requests.patch(url, files=files_to_send)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    res = response.json()
    try:
        person_camera = res["person_camera"]
        if person_camera:
            id_camera = person_camera["id_camera"]
            id_person_camera = person_camera["id_person_camera"]
            type = person_camera["type"]
            id_image = "123"
            url = settings.SERVER_FACE + "/person_image/update_image/" + id_image
            service_exist = service_services.get(id=id_camera)
            if service_exist:
                data_send = {
                    "id_person": id_person,
                    "key_camera": type,
                    "host_camera": str(service_exist.server.ip_address),
                    "port_camera": str(service_exist.port),
                    "username_camera": "",
                    "password_camera": "",
                    "id_person_camera": id_person_camera,
                }

                requests.put(url, json=data_send)
    except Exception:
        pass

    return res["data"]


@router.post("/check_image_valid")
async def check_image_valid(file: UploadFile = File(...)):
    file = await file.read()
    check_one_face(file)
    return True


@router.delete("/delete_image/{id_person}/{id_image}")
async def delete_image(id_person: str, id_image: str):
    url = (
        settings.SERVER_FACE
        + "/person_image/delete_image/"
        + id_person
        + "/"
        + id_image
    )
    response = requests.delete(url)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json()["detail"])
    data = response.json()
    url = settings.SERVER_FACE + "/person_image/update_image/" + id_image
    for item in data:
        try:
            type = item["type"]
            id_camera = item["id_camera"]
            id_person_camera = item["id_person_camera"]
            if type != "FACE_SERVICE":
                camera = camera_services.get(id=id_camera)
                if not camera:
                    continue
                data_send = {
                    "id_person": id_person,
                    "key_camera": type,
                    "host_camera": camera.ip_address,
                    "port_camera": str(camera.port),
                    "username_camera": camera.username,
                    "password_camera": camera.password,
                    "id_person_camera": id_person_camera,
                }
            else:
                service_exist = service_services.get(id=id_camera)
                if not service_exist:
                    continue
                data_send = {
                    "id_person": id_person,
                    "key_camera": type,
                    "host_camera": str(service_exist.server.ip_address),
                    "port_camera": str(service_exist.port),
                    "username_camera": "",
                    "password_camera": "",
                    "id_person_camera": id_person_camera,
                }

            requests.put(url, json=data_send)
        except Exception:
            continue

    return response.json()
