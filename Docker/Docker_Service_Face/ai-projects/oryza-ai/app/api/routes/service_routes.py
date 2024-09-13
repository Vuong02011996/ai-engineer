from typing import Any

from fastapi import APIRouter, Depends
from app.api import deps
from app.schemas.service_schemas import (
    ServiceCreate,
    ServiceUpdate,
    ServiceOut,
    ListServiceOut,
)
from app.schemas.base_schemas import Msg

# from app.services import service_services
from app.services.service_services import service_services

router = APIRouter()


@router.post(
    "/create",
    response_model=ServiceOut,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def create_service(
    request: ServiceCreate,
) -> ServiceOut:
    return service_services.create_service(request)


@router.get(
    "/get_all",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
    response_model=ListServiceOut,
)
def get_all_service(
    page: int = 0,
    page_break: bool = False,
) -> ListServiceOut:
    return {"data": service_services.get_services(page=page, page_break=page_break)}


@router.get(
    "/get_by_server",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
    response_model=ListServiceOut,
)
def get_services_by_server(
    server_id,
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
) -> Any:
    return {
        "data": service_services.get_services_by_server_page(
            server_id=server_id,
            page=page,
            page_break=page_break,
            data_search=data_search,
        )
    }


@router.get(
    "/get_count_by_server",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
    response_model=Any,
)
def count_services_by_server(
    server_id,
    data_search: str = None,
) -> Any:
    return {
        "count": service_services.get_count_services_by_server_page(
            server_id=server_id, data_search=data_search
        )
    }


@router.get("/get_by_server_id/{server_id}")
def get_by_server_id(server_id: str):
    return service_services.get_services_by_server_id(server_id=server_id)


@router.get(
    "/get_by_id/{service_id}",
    response_model=ServiceOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_by_id(
    service_id: str,
) -> ServiceOut:
    return service_services.get_service(id=service_id)


@router.get(
    "/get_info_by_id/{service_id}",
    response_model=Any,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_info_by_id(
    service_id: str,
) -> Any:
    return service_services.get_service(id=service_id)


@router.put(
    "/update_by_id/{service_id}",
    response_model=ServiceOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def update_service(
    service_id: str,
    request: ServiceUpdate,
) -> ServiceOut:
    return service_services.update_service(id=service_id, data=request)


@router.delete(
    "/delete_by_id/{service_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def delete_user(service_id: str) -> Msg:
    service_services.remove_service(id=service_id)
    return {"msg": "Service deleted"}
