from fastapi import APIRouter, File, Form
from typing_extensions import Annotated, Optional

from app.common.enum import SexEnum
from app.services.person_dahua_service import person_dahua_service
from app.schemas.person_dahua_schema import (
    CreatePerson,
    UpdatePerson,
    DeletePerson,
    OutsPerson,
)

router = APIRouter()


@router.post("/create")
async def create_person(
    file: Annotated[bytes, File()],
    host: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    group_id: Annotated[str, Form()],
    name: Annotated[str, Form()],
    sex: Annotated[Optional[SexEnum], Form()] = None,
    birthday: Annotated[str, Form()] = None,
    country: Annotated[str, Form()] = None,
    city: Annotated[str, Form()] = None,
):
    data = CreatePerson()
    data.image = file
    data.host = host
    data.username = username
    data.password = password
    data.group_id = group_id
    data.name = name
    data.sex = sex.value if sex is not None else None
    data.birthday = birthday
    data.country = country
    data.city = city
    return person_dahua_service.create_preson(data)


@router.put("/update")
async def update_person(
    file: Annotated[bytes, File()] = None,
    uid: str = Form(...),
    host: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    group_id: str = Form(...),
    name: Annotated[str, Form()] = None,
    sex: Annotated[Optional[SexEnum], Form()] = None,
    birthday: Annotated[str, Form()] = None,
    country: Annotated[str, Form()] = None,
    city: Annotated[str, Form()] = None,
):
    # if uid == None:
    #     raise  HTTPException(status_code=400, detail="uid is required")
    # if host == None:
    #     raise  HTTPException(status_code=400, detail="host is required")
    # if username == None:
    #     raise  HTTPException(status_code=400, detail="username is required")
    data = UpdatePerson()
    data.uid = uid
    data.image = file
    data.host = host
    data.username = username
    data.password = password
    data.group_id = group_id
    data.name = name
    data.sex = sex.value if sex is not None else None
    data.birthday = birthday
    data.country = country
    data.city = city
    return person_dahua_service.update_person(data)


@router.post("/delete")
async def delete_person(request: DeletePerson):
    return person_dahua_service.delete_person(request)


@router.post("/get_all")
async def get_all(request: OutsPerson):
    return person_dahua_service.get_all(request)
