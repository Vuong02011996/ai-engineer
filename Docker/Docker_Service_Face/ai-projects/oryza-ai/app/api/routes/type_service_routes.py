from fastapi import APIRouter, Depends
from app.schemas.base_schemas import Msg
from app.schemas.type_service_schemas import (
    TypeServiceUpdate,
    TypeServiceCreate,
    TypeServiceOut,
    ListTypeServiceOut,
)

# from app.services import type_service_services
from app.services.type_service_services import type_service_services
from app.api import deps

router = APIRouter()


@router.post(
    "/create",
    response_model=TypeServiceOut,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def create_type_service(request: TypeServiceCreate) -> TypeServiceOut:
    return type_service_services.create_type_service(request)


@router.get(
    "/get_all",
    response_model=ListTypeServiceOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_user)],
)
def get_all_type_service(
    page: int = 0,
    page_break: bool = False,
    data_search: str = None,
):
    return {
        "data": type_service_services.get_type_services(
            page=page, page_break=page_break, data_search=data_search
        )
    }


@router.get(
    "/get_by_id/{type_service_id}",
    response_model=TypeServiceOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_by_id(
    type_service_id: str,
) -> TypeServiceOut:
    return type_service_services.get_type_service(id=type_service_id)


@router.get(
    "/count",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def count_type_service(
    data_search: str = None,
):
    return {"count": type_service_services.count_type_services(data_search=data_search)}


@router.put(
    "/update_by_id/{type_service_id}",
    response_model=TypeServiceOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def update_type_service(
    type_service_id: str,
    request: TypeServiceUpdate,
) -> TypeServiceOut:
    return type_service_services.update_type_service(id=type_service_id, data=request)


@router.delete(
    "/delete_by_id/{type_service_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
    response_model=Msg,
)
def delete_by_id(
    type_service_id: str,
) -> Msg:
    type_service_services.remove_type_service(id=type_service_id)
    return {"msg": "Type service deleted"}
