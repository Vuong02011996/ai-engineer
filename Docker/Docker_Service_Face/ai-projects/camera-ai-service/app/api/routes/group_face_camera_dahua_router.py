from fastapi import APIRouter

from app.services.face_group_dahua_service import face_group_dahua_service
from app.schemas.base_face_camera_dahua import BaseCameraDahua
from app.schemas.face_group_dahua_schema import CreateFaceGroup, UpdateFaceGroup, DeleteFaceGroup
router = APIRouter()


@router.post("/create")
async def create_group(request: CreateFaceGroup):
    return face_group_dahua_service.create_face_group(request)


@router.put("/update")
async def update_group(request: UpdateFaceGroup):
    return face_group_dahua_service.update_face_group(request)


@router.post("/delete")
async def delete_group(request: DeleteFaceGroup):
    return face_group_dahua_service.delete_face_group(request)


@router.post("/get_all")
async def get_all(request: BaseCameraDahua):
    return face_group_dahua_service.get_all(request)
