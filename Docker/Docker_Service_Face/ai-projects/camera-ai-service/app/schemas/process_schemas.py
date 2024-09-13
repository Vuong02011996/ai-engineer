from pydantic import BaseModel


class StartProcess(BaseModel):
    """Input process_id and camera configuration to start a process."""

    process_id: str
    brand_camera_key: str  # look in app.common.Enum.type_camera
    ip_address: str
    port: int | None = None
    username: str
    password: str


class Process(BaseModel):
    process_id: str
    brand_camera_key: str  # look in app.common.Enum.type_camera
    ip_address: str
    port: int | None = None
    username: str
    password: str


class StopProcess(BaseModel):
    process_id: str


class ProcessOutBase(BaseModel):
    process_id: str
    status: str


class ProcessEnableOut(ProcessOutBase):
    pid: str


class ProcessKillOut(ProcessOutBase):
    pass
