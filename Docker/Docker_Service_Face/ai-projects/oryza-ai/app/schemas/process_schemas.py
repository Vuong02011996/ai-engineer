from typing import Optional
from odmantic import ObjectId
from datetime import datetime
from pydantic import field_validator

from app.schemas.base_schemas import BaseSchema
from app.common.constants.enums import ProcessStatus
from app.models.camera_model import Camera
from app.models.service_model import Service


class ProcessBase(BaseSchema):
    camera: Optional[str] = None
    service: Optional[str] = None
    status: Optional[ProcessStatus] = ProcessStatus.stop
    isEnable: Optional[bool] = False
    pid: Optional[str] = None
    id_type_service: Optional[str] = None


class ProcessCreate(BaseSchema):
    camera_id: str
    service_id: str
    id_type_service: Optional[str] = None
    rtsp: Optional[str] = None


class ProcessRun(BaseSchema):
    process_id: str
    is_debug: Optional[bool] = False


class ProcessKill(BaseSchema):
    process_id: str


class ProcessUpdate(BaseSchema):
    service_id: Optional[str] = None
    status: Optional[ProcessStatus] = None

    @field_validator("status", mode="before")
    def empty_str_to_none_status(cls, v):
        return None if v == "" else v


class ProcessInDBBase(ProcessBase):
    id: ObjectId
    camera: Camera
    service: Service


class ProcessInDB(ProcessInDBBase):
    pass


class ProcessOut(ProcessInDBBase):
    created: datetime
    modified: datetime
    camera: str
    service: dict

    @field_validator("camera", mode="before")
    def convert_camera_to_id(cls, v):
        return str(v.id) if v else None

    @field_validator("service", mode="before")
    def convert_service_to_id(cls, v):
        type_service = v.type_service
        return (
            {
                "id": str(v.id),
                "name": v.name,
                "type_service": {
                    "id": str(type_service.id),
                    "name": type_service.name,
                    "key": type_service.key,
                },
            }
            if v
            else None
        )


class ListProcessOut(BaseSchema):
    data: list[ProcessOut]
