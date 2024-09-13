from fastapi import APIRouter, File

from app.common.image_face import check_one_face
from app.schemas.person_image_schemas import PersonImageUpdateAuto
from app.services.person_image_service import person_image_services
from fastapi import UploadFile

router = APIRouter()


@router.patch("/create/{id_person}")
async def create_image_by_person(id_person: str, files: UploadFile = File(...)):
    return await person_image_services.create_image_by_person(
        id_person=id_person, file=files
    )


@router.post("/check_image_valid")
async def check_image_valid(file: UploadFile = File(...)):
    file = await file.read()
    check_one_face(file)
    return True


@router.delete("/delete_image/{id_person}/{id_image}")
async def delete_image(id_person: str, id_image: str):
    return await person_image_services.delete_image(
        id_person=id_person, id_image=id_image
    )


@router.put("/update_image/{id_image}")
def update_image(res: PersonImageUpdateAuto, id_image: str):
    return person_image_services.update_image(id_image=id_image, res=res)
