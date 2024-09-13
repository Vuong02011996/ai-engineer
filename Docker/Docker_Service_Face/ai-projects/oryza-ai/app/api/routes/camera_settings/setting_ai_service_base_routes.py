from fastapi import APIRouter, Depends
from app.api import deps
from app.models import User
from app.common.constants.filter_setting_crow_enum import FilterSettingCrow


def get_routes(
    create_schema,
    update_schema,
    services,
):
    router = APIRouter()

    @router.post(
        "/create",
        status_code=201,
    )
    def create_setting(
        request: create_schema,
        current_user: User = Depends(deps.get_current_active_admin),
    ):
        request.company_id = str(current_user.company.id)
        return services.create_setting(res=request)

    @router.put(
        "/update/{setting_id}",
        status_code=200,
        dependencies=[Depends(deps.get_current_active_admin)],
    )
    def update_setting(
        setting_id: str,
        request: update_schema,
    ):
        return services.update_setting(request, setting_id)

    @router.get(
        "/get_by_camera/{camera_id}/{key_ai}",
        status_code=200,
        dependencies=[Depends(deps.get_current_active_admin)],
    )
    def get_by_camera_id(camera_id: str, key_ai: str):
        return services.get_by_camera(camera_id, key_ai)

    @router.get(
        "/get_all/{key_ai}",
        status_code=200,
    )
    def get_all(
        key_ai: str,
        current_user: User = Depends(deps.get_current_active_admin),
    ):
        return services.get_all(
            company_id=str(current_user.company.id),
            key_ai=key_ai,
        )

    @router.get(
        "/get_all_info",
        status_code=200,
    )
    def get_all_info(
        page: int = 0,
        page_break: bool = False,
        data_search: str = None,
        filter: FilterSettingCrow = FilterSettingCrow.ALL,
        current_user: User = Depends(deps.get_current_active_admin),
    ):
        return services.get_all_info(
            user=current_user,
            page=page,
            page_break=page_break,
            data_search=data_search,
            filter=filter,
        )

    @router.get(
        "/get_count_info",
        status_code=200,
    )
    def get_count_info(
        data_search: str = None,
        filter: FilterSettingCrow = FilterSettingCrow.ALL,
        current_user: User = Depends(deps.get_current_active_admin),
    ):
        return services.get_count_info(
            user=current_user, data_search=data_search, filter=filter
        )

    return router
