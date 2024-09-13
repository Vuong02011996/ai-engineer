from app.schemas.base_schemas import BaseSchema
from typing import Optional


class EstimateTimeRequest(BaseSchema):
    fps: int
    video_length: int  # in seconds
    width: int
    height: int
    type: str
    skip_frames: int = 0


class AnalyzeVideoRequest(EstimateTimeRequest):
    video_url: str
    rbmq_url: Optional[str] = None
    rbmq_exchange_key: Optional[str] = None
    rbmq_progress_info_key: Optional[str] = None
    rbmq_username: Optional[str] = None
    rbmq_password: Optional[str] = None
    webhook_url: Optional[str] = None
    image_extension: Optional[str] = None
    black_list: Optional[list] = None
