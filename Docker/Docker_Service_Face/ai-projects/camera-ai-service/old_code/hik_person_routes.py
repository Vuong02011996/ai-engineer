from fastapi import APIRouter
import requests
from app.schemas.hik_camera_schema import HikFaceCreate, FaceInput, Camera
from app.services.hik_services import hik_services

router = APIRouter()


@router.post("/add_face")
async def create_person(request: HikFaceCreate):
    """For testing purposes only. Add a face to the Hikvision camera."""
    camera = Camera(
        username=request.username,
        password=request.password,
        ip_address=request.ip_address,
        port=request.port,
    )
    # Fetch the image data from the URL
    response = requests.get(request.image_url)
    image = response.content
    face_input = FaceInput(name=request.name, person_id=request.person_id, image=image)
    return hik_services.add_face(face_input, camera)
