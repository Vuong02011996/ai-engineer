from fastapi import APIRouter, Depends
from app.schemas.base_schemas import Msg
from app.schemas.vms_schemas import VMSCreate, VMSUpdate, VMSOut
from app.services.vms_services import vms_services
from app.api import deps

router = APIRouter()


@router.post(
    "/create",
    status_code=201,
    response_model=VMSOut,
)
def create_vms(
    request: VMSCreate,
    current_user: deps.User = Depends(deps.get_current_active_admin),
) -> VMSOut:
    return vms_services.create_vms(obj_in=request, user=current_user)


@router.get(
    "/get_by_id/{vms_id}",
    response_model=VMSOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def read_vms(
    vms_id: str,
) -> VMSOut:
    return vms_services.get_by_id(id=vms_id)


@router.get(
    "/get_my_company_vms",
    response_model=VMSOut,
    status_code=200,
)
def read_my_company_vms(
    current_user: deps.User = Depends(deps.get_current_active_admin),
) -> VMSOut:
    return vms_services.get_my_company_vms(user=current_user)


@router.get(
    "/get_all",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def read_vmss():
    return {"data": vms_services.get_vms_all()}


@router.get(
    "/count",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def count_vmss():
    return {"count": vms_services.count_vms()}


@router.put(
    "/update_by_id/{vms_id}",
    response_model=VMSOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def update_vms(
    vms_id: str,
    request: VMSUpdate,
) -> VMSOut:
    return vms_services.update_by_id(id=vms_id, obj_in=request)


@router.put(
    "/update_my_company_vms",
    response_model=VMSOut,
    status_code=200,
)
def update_my_company_vms(
    request: VMSUpdate,
    current_user: deps.User = Depends(deps.get_current_active_admin),
) -> VMSOut:
    return vms_services.update_my_company_vms(obj_in=request, user=current_user)


@router.delete(
    "/delete_my_company_vms",
    status_code=200,
)
def delete_my_company_vms(
    current_user: deps.User = Depends(deps.get_current_active_admin),
):
    vms_services.remove_my_company_vms(user=current_user)
    return Msg(msg="VMS deleted")


@router.delete(
    "/delete_by_id/{vms_id}",
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_vms(vms_id: str):
    vms_services.remove_vms(id=vms_id)
    return Msg(msg="VMS deleted")
