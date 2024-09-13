from typing import Any

from fastapi import APIRouter, Depends

from app.api import deps
from app.models import User
from app.schemas import Count
from app.schemas.event_schemas import EventUpdateFace, SearchCondition

# from app.services import event_services
from app.services.event_services import event_services

router = APIRouter()


# @router.get("/get_by_id/{event_id}", response_model=Any, status_code=200)
# def read_event(
#     event_id: str,
#     # current_user: User = Depends(deps.get_current_active_user),
# ) -> Any:
#     return event_services.get_by_id(id=event_id)


@router.get(
    "/get_by_type_service/{type_service_id}",
    status_code=200,
    response_model=Any,
)
def get_all(
    type_service_id: str,
    page: int = 0,
    page_break: bool = False,
    start_time: str = None,
    end_time: str = None,
    data_search=None,
    filter=None,
    current_user: User = Depends(deps.get_current_active_user),
):
    result = event_services.get_by_type_service(
        user=current_user,
        type_service_id=type_service_id,
        page=page,
        page_break=page_break,
        start_time=start_time,
        end_time=end_time,
        data_search=data_search,
        filter=filter,
    )
    data_result = []
    for item in result:
        data = {
            "id": str(item.id),
            "data": item.data,
            "camera": str(item.camera),  # this field is actually camera_id
            "created": item.created,
        }
        data_result.append(data)
    return {"data": data_result}


@router.get(
    "/get_count_by_type_service/{type_service_id}",
    status_code=200,
    response_model=Count,
)
def get_count(
    type_service_id: str,
    start_time: str = None,
    end_time: str = None,
    data_search=None,
    filter=None,
    current_user: User = Depends(deps.get_current_active_user),
):
    result = event_services.get_count(
        user=current_user,
        type_service_id=type_service_id,
        start_time=start_time,
        end_time=end_time,
        data_search=data_search,
        filter=filter,
    )
    return Count(count=result)


@router.put("/face_recognition", status_code=200)
def update_face_recognition(
    data: EventUpdateFace,
    # current_user: User = Depends(deps.get_current_active_user),
):
    return event_services.update_face_recognition(data=data)


@router.get("/record/{event_id}", status_code=200)
def get_record_media(
    event_id: str,
    # current_user: User = Depends(deps.get_current_active_user),
):
    return event_services.get_record(event_id)


@router.post("/get_event_image", status_code=200)
async def get_images(
    search_condition: SearchCondition,
):
    rs = await event_services.download_images_from_event(search_condition)
    return {"data": rs}


# for anpr service
@router.get("/get_plate_number/{camera_id}", status_code=200)
def get_plate_number(
    camera_id: str,
    start_time: int = None,
    end_time: int = None,
):
    rs = event_services.get_plate_number(camera_id, start_time, end_time)
    return {"data": rs}
