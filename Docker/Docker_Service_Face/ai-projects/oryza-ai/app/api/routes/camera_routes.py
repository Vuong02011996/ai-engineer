from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from odmantic import ObjectId

from app.schemas.camera_schemas import (
    CameraOut,
    CameraCreate,
    CameraUpdate,
    GenerateRTSP,
)
from app.schemas import ListCameraOut
from app.schemas.base_schemas import Count, Msg
from app.models.user_model import User
from app.services.camera_services import camera_services
from app.api import deps

router = APIRouter()


# CREATE camera
@router.post("/create", response_model=CameraOut, status_code=201)
def create_camera(
    request: CameraCreate,
    current_user: User = Depends(deps.get_current_active_admin),
) -> CameraOut:
    return camera_services.create_camera(user=current_user, obj_in=request)


# READ camera
@router.get(
    "/get_by_id/{camera_id}",
    response_model=CameraOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def read_camera(
    camera_id: str,
) -> CameraOut:
    return camera_services.get_camera(id=camera_id)


@router.get("/count", status_code=200, response_model=Count)
def count_camera(
    current_user: User = Depends(deps.get_current_active_admin),
    data_search: str = None,
) -> Count:
    return Count(
        count=camera_services.count_camera(user=current_user, data_search=data_search)
    )


@router.get("/get_all", response_model=ListCameraOut, status_code=200)
def read_cameras(
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    return {
        "data": camera_services.get_cameras(
            user=current_user, page=page, page_break=page_break, data_search=data_search
        )
    }


@router.get("/get_by_company_id/{company_id}", status_code=200)
def read_cameras_by_company(
    company_id: str,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    return {
        "data": camera_services.get_cameras_by_company(
            user=current_user, company_id=company_id
        )
    }


@router.get(
    "/get_by_geo_unit/{geo_unit_id}", response_model=ListCameraOut, status_code=200
)
def get_by_geo_unit(geo_unit_id: str):
    return {"data": camera_services.get_by_geo_unit(geo_unit_id)}


@router.get("/get_camera_face_ai")
def get_camera_face_ai(
    data_search: str = None,
    current_user: User = Depends(deps.get_current_active_admin),
):
    return camera_services.get_by_face_ai(
        company_id=current_user.company.id, data_search=data_search
    )


@router.get(
    "/get_camera_face_ai/{company_id}",
    dependencies=[Depends(deps.get_current_active_admin)],
    status_code=200,
)
def get_camera_face_ai_by_company(
    company_id: str,
):
    try:
        company_id = ObjectId(company_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Company not found")
    return camera_services.get_by_face_ai(company_id=company_id)


# UPDATE camera
@router.put(
    "/update_by_id/{camera_id}",
    response_model=CameraOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def update_camera(
    camera_id: str,
    request: CameraUpdate,
) -> CameraOut:
    return camera_services.update_camera(id=camera_id, obj_in=request)


# DELETE camera
@router.delete(
    "/delete_by_id/{camera_id}",
    status_code=200,
    response_model=Msg,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_camera(
    camera_id: str,
) -> Msg:
    camera_services.remove_camera(id=camera_id)
    return {"msg": "Camera deleted"}


# sync camera from vms
@router.get("/sync-from-vms", status_code=200)
def sync_camera_vms(
    current_user: User = Depends(deps.get_current_active_admin),
):
    return camera_services.sync_from_vms(user=current_user)


@router.post(
    "/generate_rtsp",
    status_code=201,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def generate_rtsp(
    rq: GenerateRTSP,
):
    return camera_services.generate_rtsp(rq)


@router.get(
    "/get_list_rtsp/{camera_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def list_rtsp(camera_id: str):
    return camera_services.get_list_rtsp(camera_id)


@router.get("/get_hls_stream/{camera_id}", status_code=200)
def get_hls_stream(camera_id: str):
    return camera_services.get_hls_stream(camera_id)


@router.get("/get_video_record/{camera_id}", status_code=200)
def get_video_record(camera_id: str, start_time: int, duration: int):
    return camera_services.get_video_record(camera_id, start_time, duration)
