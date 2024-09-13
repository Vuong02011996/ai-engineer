from fastapi import APIRouter, Depends

from app.api import deps

# from app.services import brand_camera_services
from app.services.brand_camera_services import brand_camera_services

from app.schemas.base_schemas import Count, Msg
from app.schemas.brand_camera_schemas import (
    BrandCameraCreate,
    BrandCameraUpdate,
    BrandCameraOut,
    ListBrandCameraOut,
)

router = APIRouter()


@router.post(
    "/create",
    response_model=BrandCameraOut,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def create_brand_camera(brand_camera_in: BrandCameraCreate):
    return brand_camera_services.create_brand_camera(obj_in=brand_camera_in)


@router.get(
    "/get_by_id/{brand_camera_id}",
    response_model=BrandCameraOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def read_brand_camera(
    brand_camera_id: str,
) -> BrandCameraOut:
    return brand_camera_services.get_brand_camera(id=brand_camera_id)


@router.get(
    "/count",
    status_code=200,
    response_model=Count,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def count_brand_camera(data_search: str = None):
    return {"count": brand_camera_services.count_brand_camera(data_search=data_search)}


@router.get(
    "/get_all",
    response_model=ListBrandCameraOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def read_brand_cameras(
    page: int = 0, page_break: bool = False, data_search: str = None
):
    return {
        "data": brand_camera_services.get_brand_cameras(
            page=page, page_break=page_break, data_search=data_search
        )
    }


@router.put(
    "/update_by_id/{brand_camera_id}",
    response_model=BrandCameraOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def update_brand_camera(
    brand_camera_id: str,
    brand_camera_in: BrandCameraUpdate,
) -> BrandCameraOut:
    return brand_camera_services.update_brand_camera(
        id=brand_camera_id, obj_in=brand_camera_in
    )


@router.delete(
    "/delete_by_id/{brand_camera_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_brand_camera(
    brand_camera_id: str,
) -> Msg:
    brand_camera_services.delete_brand_camera(id=brand_camera_id)
    return {"msg": "Brand Camera deleted"}
