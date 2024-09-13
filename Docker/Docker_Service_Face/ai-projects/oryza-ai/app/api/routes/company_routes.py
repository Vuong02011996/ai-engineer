from fastapi import APIRouter, Depends
from app.schemas.base_schemas import Count, Msg
from app.schemas.company_schemas import (
    CompanyOut,
    CompanyCreate,
    CompanyUpdate,
    ListCompanyOut,
)
from app.models.user_model import User

# from app.services import company_services
from app.services.company_services import company_services
from app.api import deps


router = APIRouter()


# CREATE company
@router.post(
    "/create",
    response_model=CompanyOut,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def create_company(request: CompanyCreate) -> CompanyOut:
    company = company_services.create_company(obj_in=request)
    return company


# READ company
@router.get(
    "/get_by_id/{company_id}",
    response_model=CompanyOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def get_company(company_id: str) -> CompanyOut:
    company = company_services.get_company(id=company_id)
    return company


@router.get("/get_my_company", response_model=CompanyOut, status_code=200)
def get_my_company(
    current_user: User = Depends(deps.get_current_active_user),
) -> CompanyOut:
    return current_user.company


@router.get(
    "/get_all",
    response_model=ListCompanyOut,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def get_companies(page: int = 0, page_break: bool = False, data_search: str = None):
    return {
        "data": company_services.get_companies(
            page=page, page_break=page_break, data_search=data_search
        )
    }


@router.get(
    "/count",
    status_code=200,
    response_model=Count,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def count_companies(data_search: str = None):
    return {"count": company_services.count_company(data_search=data_search)}


# UPDATE company
@router.put(
    "/update_by_id/{company_id}",
    response_model=CompanyOut,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def update_company(
    company_id: str,
    request: CompanyUpdate,
) -> CompanyOut:
    company = company_services.update_company(id=company_id, obj_in=request)
    return company


# DELETE company
@router.delete(
    "/delete_by_id/{company_id}",
    status_code=200,
    response_model=Msg,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def delete_company(company_id: str) -> Msg:
    company_services.remove_company(id=company_id)
    return {"msg": "Company deleted"}
