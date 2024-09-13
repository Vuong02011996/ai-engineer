from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.api import deps
from app.models.user_model import User
from app.schemas.camera_settings.setting_uniforms_company import (
    SettingUniformsCompanyUpdate,
    SettingUniformsCompanyDeleteImage,
)
from app.services.camera_settings.setting_uniform_company_services import (
    setting_uniform_company_services,
)

router = APIRouter()


# CREATE camera
@router.post("/create", status_code=201)
async def create_camera(
    files: List[UploadFile] = None,
    rgb: str = Form(...),
    current_user: User = Depends(deps.get_current_active_admin),
):
    return await setting_uniform_company_services.create_setting(
        files=files, rgb=rgb, user=current_user
    )


@router.put(
    "/update/{id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
async def update_camera(
    request: SettingUniformsCompanyUpdate,
    id: str,
):
    return setting_uniform_company_services.update_setting(id=id, obj_in=request)


@router.put("/update_image/{id}")
async def update_image(
    id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_company_services.update_image(id=id, image=file)


@router.delete("/delete_image/{id}")
async def delete_image(
    id: str,
    request: SettingUniformsCompanyDeleteImage,
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_company_services.delete_image(
        id=id, image_id=request.image_url
    )


@router.get("/get_by_company")
async def get_by_company(
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_company_services.get_by_id_company(
        str(current_user.company.id)
    )


@router.delete("/delete")
async def delete_camera(
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_company_services.delete(user=current_user)
