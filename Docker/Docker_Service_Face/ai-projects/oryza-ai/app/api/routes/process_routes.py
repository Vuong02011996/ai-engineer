from typing import Any

from fastapi import APIRouter, Depends
from app.schemas.base_schemas import Msg
from app.schemas.process_schemas import (
    ProcessOut,
    ProcessCreate,
    ProcessUpdate,
    ProcessRun,
    ListProcessOut,
)
from app.models.user_model import User

from app.services.process_services import process_services
from app.api import deps

router = APIRouter()


@router.post(
    "/run", response_model=Any, dependencies=[Depends(deps.get_current_active_admin)]
)
def run_process(
    request: ProcessRun,
):
    return process_services.run_process(obj_in=request)


@router.post("/kill/{process_id}")
def kill_process(
    process_id: str,
    current_user: User = Depends(deps.get_current_active_admin),
):
    return process_services.kill_process(user=current_user, process_id=process_id)


@router.post("/create", response_model=ProcessOut, status_code=201)
def create_process(
    request: ProcessCreate,
    current_user: User = Depends(deps.get_current_active_admin),
) -> ProcessOut:
    return process_services.create_process(user=current_user, obj_in=request)


@router.get("/get_by_id/{process_id}", response_model=ProcessOut, status_code=200)
def read_process(
    process_id: str,
    current_user: User = Depends(deps.get_current_active_admin),
) -> ProcessOut:
    process = process_services.get_process(user=current_user, id=process_id)
    return process


@router.get("/get_all", response_model=ListProcessOut, status_code=200)
def read_processes(
    page: int = 0,
    page_break: bool = False,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    return {
        "data": process_services.get_processes(
            page=page,
            page_break=page_break,
            user=current_user,
        )
    }


@router.get(
    "/get_by_id_type_service/{id_type_service}", response_model=Any, status_code=200
)
def get_by_id_type_service(
    id_type_service: str,
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    return process_services.get_by_id_type_service(
        page=page,
        page_break=page_break,
        user=current_user,
        id_type_service=id_type_service,
        data_search=data_search,
    )


@router.get(
    "/get_count_by_id_type_service/{id_type_service}",
    response_model=Any,
    status_code=200,
)
def count_by_id_type_service(
    id_type_service: str,
    data_search: str = None,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    return process_services.get_count_by_id_type_service(
        user=current_user, id_type_service=id_type_service, data_search=data_search
    )


@router.get(
    "/get_by_camera_id/{camera_id}", response_model=ListProcessOut, status_code=200
)
def read_processes_by_camera(
    camera_id: str,
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    return {
        "data": process_services.get_processes_by_camera_id(
            camera_id=camera_id,
            user=current_user,
        )
    }


@router.put("/update_by_id/{process_id}", response_model=ProcessOut, status_code=200)
def update_process(
    process_id: str,
    request: ProcessUpdate,
    current_user: User = Depends(deps.get_current_active_admin),
) -> ProcessOut:
    process = process_services.update_process(
        id=process_id, obj_in=request, user=current_user
    )
    return process


@router.delete("/delete_by_id/{process_id}", status_code=200)
def delete_process(
    process_id: str, current_user: User = Depends(deps.get_current_active_admin)
) -> Msg:
    """Kill process, then delete it from database"""
    process_services.remove_process(user=current_user, id=process_id)
    return {"msg": "Process deleted"}


@router.get(
    "/preview_image_process/{process_id}",
    status_code=200,
    # dependencies=[Depends(deps.get_current_active_admin)]
)
def preview_image_process(
    process_id: str,
):
    return process_services.get_preview_image_by_process_id(process_id)
