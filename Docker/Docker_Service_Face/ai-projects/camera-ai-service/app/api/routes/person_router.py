from typing import List
from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.person_schemas import PersonUpdate, PersonRegister, PersonModify
from app.services.person_service import person_services

router = APIRouter()


@router.post("/create")
async def create_person(
    files: List[UploadFile] = File(...),
    id_company: str = Form(...),
    name: str = Form(...),
    other_info: str = Form(None),
):
    other_info_dict = person_services.check_info_other(other_info)
    return await person_services.create_person(
        obj_in={"company_id": id_company, "name": name, "other_info": other_info_dict},
        files=files,
    )


@router.post("/register/{id_company}")
async def register_person(data: PersonRegister, id_company: str):
    print(data)
    return person_services.register_person(data=data, id_company=id_company)


@router.put("/modifier/{id_company}")
async def modifier_person(data: PersonModify, id_company: str):
    print(data)
    return person_services.modifier_person(data=data, id_company=id_company)


@router.put("/update/{id_person}")
async def update_person(data: PersonUpdate, id_person: str):
    return person_services.update_person(obj_in=data, id_person=id_person)


@router.delete("/delete/{id_person}")
async def delete_person(id_person: str):
    return person_services.delete_person(id_person=id_person)


@router.get("/get_by_company/{id_company}")
async def get_person_by_company(
    id_company: str, page: int = 0, page_break: bool = False, data_search: str = None
):
    return person_services.get_person_by_company(
        id_company=id_company, page=page, page_break=page_break, data_search=data_search
    )

@router.get("/get_person_by_company_camera/{id_company}")
async def get_person_by_company_camera(
    id_company: str, id_camera: str, page: int = 0, page_break: bool = False, data_search: str = None,filter: str = None
):
    return person_services.get_person_by_company_camera(
        id_company=id_company, page=page, page_break=page_break, data_search=data_search, id_camera=id_camera,filter=filter
    )

@router.get("/get_count_person_by_company_camera/{id_company}")
async def get_count_person_by_company_camera(
    id_company: str, id_camera: str,  data_search: str = None,filter: str = None
):
    return person_services.get_count_person_by_company_camera(
        id_company=id_company,  data_search=data_search, id_camera=id_camera,filter=filter
    )


@router.get("/async_user/{id_company}")
async def async_user(id_company: str):
    return person_services.async_user(id_company=id_company)


@router.get("/get_count_by_company/{id_company}")
async def get_count_by_company(id_company: str, data_search: str = None):
    return person_services.get_count_by_company(
        id_company=id_company, data_search=data_search
    )


@router.get("/get_by_id/{id_person}")
async def get_by_id(id_person: str):
    return person_services.get_by_id(id=id_person)


@router.get("/get_by_person_id_camera/{person_id_camera}")
async def get_by_person_id_camera(person_id_camera: str):
    return person_services.get_by_person_id_camera(person_id_camera=person_id_camera)
