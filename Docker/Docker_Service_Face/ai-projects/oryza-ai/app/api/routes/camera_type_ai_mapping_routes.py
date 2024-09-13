from typing import Any

from fastapi import APIRouter, Depends
from app.services.camera_type_ai_mapping_services import (
    camera_type_ai_mapping_services as mapping_services,
)
from app.api import deps

router = APIRouter()


@router.get(
    "/get_by_id/{camera_id}",
    response_model=Any,
    status_code=200,
    dependencies=[Depends(deps.get_current_active_user)],
)
def read_camera(
    camera_id: str,
) -> Any:
    data = mapping_services.get_mappings_by_camera(camera_id=camera_id)
    result = []
    for item in data:
        result.append(str(item.type_service.id))
    return result
