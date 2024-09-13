from typing import List
import httpx
from fastapi import APIRouter, File, Form, Depends, HTTPException
from fastapi import UploadFile
import requests
from odmantic import ObjectId

from app.common.constants.type_camera import TypeCameraEnum
from app.core.config import settings
from app.models.user_model import User
from app.api import deps
from app.schemas.person_schemas import PersonRegister, PersonModify, PersonUpdate
from app.services.company_services import company_services
from app.services.process_services import service_services, camera_services

router = APIRouter()


@router.post("/create")
async def create_person(
    files: List[UploadFile] = File(...),
    name: str = Form(...),
    other_info: str = Form(None),
    current_user: User = Depends(deps.get_current_active_admin),
):
    url = settings.SERVER_FACE + "/person/create"
    # Prepare the files for the POST request
    files_to_send = []
    for file in files:
        file_content = await file.read()
        files_to_send.append(
            ("files", (file.filename, file_content, file.content_type))
        )

    response = requests.post(
        url,
        files=files_to_send,
        data={
            "id_company": str(current_user.company.id),
            "name": name,
            "other_info": other_info,
        },
    )

    # Ensure the response from the external request is properly formatted
    response_data = response.json()
    code = response.status_code
    if code != 200 and code != 201:
        print("response_data: ", response_data)
        raise HTTPException(status_code=code, detail=response_data["detail"])

    return response_data


@router.post("/register/{id_company}")
async def register_person(data: PersonRegister, id_company: str):
    company_services.get_company(id=id_company)
    url = settings.SERVER_FACE + "/person/register/" + id_company
    cameras = camera_services.get_by_face_ai(company_id=ObjectId(id_company))
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
    data = data.dict()
    data["list_camera"] = list_camera
    response = requests.post(url, json=data)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()


@router.put("/modifier/{id_company}")
async def modifier_person(data: PersonModify, id_company: str):
    company_services.get_company(id=id_company)
    url = settings.SERVER_FACE + "/person/modifier/" + id_company
    response = requests.put(url, json=data.dict())
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    data2 = response.json()["person_camera"]
    url = settings.SERVER_FACE + "/person_image/update_image/123"
    id_person = data.user_id
    for item in data2:
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

    return response.json()["data"]


@router.put("/update/{id_person}")
async def update_person(
    data: PersonUpdate,
    id_person: str,
    current_user: User = Depends(deps.get_current_active_admin),
):
    url = settings.SERVER_FACE + "/person/update/" + id_person
    data = data.dict()
    data["id_company"] = str(current_user.company.id)
    response = requests.put(url, json=data)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()


@router.delete(
    "/delete/{id_person}", dependencies=[Depends(deps.get_current_active_admin)]
)
async def delete_person(id_person: str):
    url = settings.SERVER_FACE + "/person/delete/" + id_person
    response = requests.delete(url)
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    list_camera_person = response.json()["list_camera_person"]
    for item in list_camera_person:
        try:
            data = {}
            url = (
                settings.SERVER_FACE
                + "/person_camera/delete/"
                + item["id_person_camera"]
            )
            data["key_camera"] = item["type"]
            data["host_camera"] = ""
            data["username_camera"] = ""
            data["password_camera"] = ""
            data["port_camera"] = ""
            if item["type"] == TypeCameraEnum.face_service:
                service_exist = service_services.get(id=item["id_camera"])
                if service_exist:
                    data["host_camera"] = str(service_exist.server.ip_address)
                    data["username_camera"] = ""
                    data["password_camera"] = ""
                    data["port_camera"] = str(service_exist.port)
            else:
                camera_exist = camera_services.get(id=item["id_camera"])
                if camera_exist:
                    data["host_camera"] = camera_exist.ip_address
                    data["username_camera"] = camera_exist.username
                    data["password_camera"] = camera_exist.password
                    data["port_camera"] = str(camera_exist.port)
            requests.post(url, json=data)
        except Exception as e:
            print("Error delete person camera", e)
            continue

    return response.json()["data"]


@router.get(
    "/get_by_company/{id_company}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
async def get_person_by_company(
    id_company: str, page: int = 0, page_break: bool = False, data_search: str = None
):
    url = (
        settings.SERVER_FACE
        + f"/person/get_by_company/{id_company}?page={page}&page_break={page_break}"
    )
    if data_search:
        url += f"&data_search={data_search}"
    try:
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.response.json()
        )
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
        return {"data": []}  # Return an empty list or a default response
    except httpx.TimeoutException:
        print("The request timed out.")
        return {"data": []}  # Return an empty list or a default response

    data = response.json()
    return data


@router.get("/get_person_by_company_camera")
async def get_person_by_company_camera(
    id_camera: str,
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
    filter: str = None,
    current_user: User = Depends(deps.get_current_active_admin),
):
    id_company = str(current_user.company.id)
    url = (
        settings.SERVER_FACE
        + f"/person/get_person_by_company_camera/{id_company}?page={page}&page_break={page_break}&id_camera={id_camera}"
    )
    if data_search:
        url += f"&data_search={data_search}"
    if filter:
        url += f"&filter={filter}"

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    data = response.json()
    return data


@router.get("/get_count_person_by_company_camera")
async def get_count_person_by_company_camera(
    id_camera: str,
    data_search: str = None,
    filter: str = None,
    current_user: User = Depends(deps.get_current_active_admin),
):
    id_company = str(current_user.company.id)
    url = (
        settings.SERVER_FACE
        + f"/person/get_count_person_by_company_camera/{id_company}?id_camera={id_camera}"
    )
    if data_search:
        url += f"&data_search={data_search}"
    if filter:
        url += f"&filter={filter}"

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    data = response.json()
    return data


@router.get("/async_user/{id_company}")
async def async_user(id_company: str):
    company_services.get_company(id=id_company)
    url = settings.SERVER_FACE + f"/person/async_user/{id_company}"

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()


@router.get(
    "/get_count_by_company/{id_company}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
async def get_count_by_company(id_company: str, data_search: str = None):
    url = settings.SERVER_FACE + f"/person/get_count_by_company/{id_company}"
    if data_search:
        url += f"?data_search={data_search}"

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()


@router.get(
    "/get_by_id/{id_person}", dependencies=[Depends(deps.get_current_active_admin)]
)
async def get_by_id(id_person: str):
    url = settings.SERVER_FACE + f"/person/get_by_id/{id_person}"

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()


@router.get(
    "/get_by_person_id_camera/{person_id_camera}",
    dependencies=[Depends(deps.get_current_active_admin)],
)
async def get_by_person_id_camera(person_id_camera: str):
    url = settings.SERVER_FACE + f"/person/get_by_person_id_camera/{person_id_camera}"

    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        response = await client.get(url)

    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())

    return response.json()
