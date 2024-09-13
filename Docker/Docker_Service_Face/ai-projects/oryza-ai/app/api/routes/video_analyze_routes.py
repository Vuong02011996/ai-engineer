from fastapi import APIRouter, HTTPException
from app.schemas.video_analyze_schemas import EstimateTimeRequest, AnalyzeVideoRequest
from app.core.config import settings
import requests

router = APIRouter()


@router.post("/estimate_time", status_code=200)
async def estimate_time(request: EstimateTimeRequest):
    if request.type not in ["face", "plate"]:
        raise HTTPException(status_code=400, detail="Invalid type")
    if request.type == "face":
        server = settings.SERVER_VIDEO_ANALYZE_FACE
    elif request.type == "plate":
        server = settings.SERVER_VIDEO_ANALYZE_PLATE
    url = f"{server}/analyze_video/estimate_time"
    response = await requests.post(
        url, json=request.model_dump(), timeout=settings.VIDEO_ESTIMATE_REQUEST_TIMEOUT
    )
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()


@router.post("/", status_code=200)
async def analyze_video(request: AnalyzeVideoRequest):
    if request.type not in ["face", "plate"]:
        raise HTTPException(status_code=400, detail="Invalid type")
    if request.type == "face":
        server = settings.SERVER_VIDEO_ANALYZE_FACE
    elif request.type == "plate":
        server = settings.SERVER_VIDEO_ANALYZE_PLATE
    url = f"{server}/analyze_video"
    response = await requests.post(
        url, json=request.model_dump(), timeout=settings.VIDEO_ESTIMATE_REQUEST_TIMEOUT
    )
    code = response.status_code
    if code != 200 and code != 201:
        raise HTTPException(status_code=code, detail=response.json())
    return response.json()
