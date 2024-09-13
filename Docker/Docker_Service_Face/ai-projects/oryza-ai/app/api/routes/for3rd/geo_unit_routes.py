from fastapi import APIRouter
from app.schemas import GeoUnitGetDetail, ListGeoUnitOut
from app.services import geo_unit_services
from typing import Optional
from app.common.constants.enums import GeoUnitType

router = APIRouter()


@router.get("/count", status_code=200)
def count_geo_unit(
    type: GeoUnitType = None,
    parent_id: Optional[str] = None,
    keyword: Optional[str] = None,
):
    return geo_unit_services.count_geo_unit(type, parent_id, keyword)


@router.get(
    "",
    status_code=200,
    response_model=ListGeoUnitOut,
)
def get_units(
    page: int = 0,
    page_break: bool = False,
    parent_id: Optional[str] = None,
    type: GeoUnitType = None,
    keyword: Optional[str] = None,
):
    rs = geo_unit_services.get_units(page, page_break, type, parent_id, keyword)
    return {"data": rs}


@router.get("/{unit_id}", status_code=200, response_model=GeoUnitGetDetail)
def get_unit_by_id(unit_id: str):
    rs = geo_unit_services.get(unit_id)
    return rs
