from fastapi import APIRouter
from app.api.routes import (
    group_face_camera_dahua_router,
    add_person_camera_dahua_router,
    process_routes,
    person_router,
    person_camera_router,
    person_image_router,
)

api_router = APIRouter()
api_router.include_router(process_routes.router)

api_router.include_router(
    group_face_camera_dahua_router.router,
    prefix="/group_face_camera_dahua",
    tags=["group face camera dahua"],
)
api_router.include_router(
    add_person_camera_dahua_router.router,
    prefix="/person_camera_dahua",
    tags=["person camera dahua"],
)
api_router.include_router(person_router.router, prefix="/person", tags=["person"])
api_router.include_router(
    person_image_router.router, prefix="/person_image", tags=["person_image"]
)
api_router.include_router(
    person_camera_router.router, prefix="/person_camera", tags=["person_camera"]
)
