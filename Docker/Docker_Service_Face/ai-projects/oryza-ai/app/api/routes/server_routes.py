from fastapi import APIRouter, Depends
from app.schemas.base_schemas import Msg, Count
from app.api import deps
from app.schemas.server_schemas import (
    ServerCreate,
    ServerOut,
    ServerUpdate,
    ListServerOut,
)

# from app.services import server_services
from app.services.server_services import server_services

router = APIRouter()


@router.post(
    "/create",
    response_model=ServerOut,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def create_server(
    request: ServerCreate,
) -> ServerOut:
    return server_services.create_server(request)


@router.get(
    "/get_all",
    response_model=ListServerOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def get_all_server(
    page: int = 0,
    page_break: bool = False,
):
    return ListServerOut(
        data=server_services.get_servers(page=page, page_break=page_break)
    )


@router.get(
    "/get_by_id/{server_id}",
    response_model=ServerOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_by_id(
    server_id: str,
) -> ServerOut:
    return server_services.get_server(id=server_id)


@router.get(
    "/count",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
    response_model=Count,
)
def count_server() -> Count:
    return Count(count=server_services.count_server())


@router.put(
    "/update_by_id/{server_id}",
    response_model=ServerOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def update_server(
    server_id: str,
    request: ServerUpdate,
) -> ServerOut:
    return server_services.update_server(id=server_id, data=request)


@router.delete(
    "/delete_by_id/{server_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def delete_by_id(
    server_id: str,
) -> Msg:
    server_services.remove_server(id=server_id)
    return {"msg": "Server deleted"}
