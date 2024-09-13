from typing import Any

from fastapi import APIRouter, Depends

from app.api import deps
from app.common.constants.filter_setting_crow_enum import FilterSettingCrow
from app.models.user_model import User
from app.schemas.camera_settings.setting_uniforms_schemas import (
    SettingUniformsCreate,
    SettingUniformsUpdate,
)
from app.services.camera_settings.base_setting_service import get_image_by_id_camera
from app.services.camera_settings.setting_uniform_detection_services import (
    setting_uniform_services,
)

router = APIRouter()


# CREATE camera
@router.post(
    "/create",
    response_model=Any,
    status_code=201,
)
def create_setting(
    request: SettingUniformsCreate,
    current_user: User = Depends(deps.get_current_active_admin),
):
    request.id_company = str(current_user.company.id)
    return setting_uniform_services.create_setting(res=request)


@router.put(
    "/update/{id}",
    response_model=Any,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def update_setting_crowd_detection(
    request: SettingUniformsUpdate,
    id: str,
):
    return setting_uniform_services.update_setting(id=id, res=request)


@router.get(
    "/get_by_id_camera/{id_camera}",
    response_model=Any,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_by_id_camera(id_camera: str):
    return setting_uniform_services.get_by_id_camera(id_camera=id_camera)


@router.get(
    "/get_image_by_id_camera/{id_camera}",
    response_model=Any,
)
def get_image_by_id_camera_(id_camera: str):
    return get_image_by_id_camera(id_camera=id_camera, type="uniform")


@router.get(
    "/get_all",
    response_model=Any,
)
def get_all(
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_services.get_all(id_company=str(current_user.company.id))


@router.get(
    "/get_all_info",
    response_model=Any,
)
def get_all_info(
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
    filter: FilterSettingCrow = FilterSettingCrow.ALL,
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_services.get_all_info(
        user=current_user,
        page=page,
        page_break=page_break,
        data_search=data_search,
        filter=filter,
    )


@router.get(
    "/get_count_info",
    response_model=Any,
)
def get_count_info(
    data_search: str = None,
    filter: FilterSettingCrow = FilterSettingCrow.ALL,
    current_user: User = Depends(deps.get_current_active_admin),
):
    return setting_uniform_services.get_count_info(
        user=current_user, data_search=data_search, filter=filter
    )
