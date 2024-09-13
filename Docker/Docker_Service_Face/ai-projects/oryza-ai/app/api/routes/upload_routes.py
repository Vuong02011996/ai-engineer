from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.api import deps
from app.common.utils.minio_services import minio_services

router = APIRouter()


@router.post(
    "/upload", dependencies=[Depends(deps.get_current_active_admin)], status_code=201
)
def upload_file(
    file: UploadFile = File(...),
):
    file_name = ".".join(file.filename.split(".")[:-1])
    try:
        url = minio_services.upload_file_form(file_name, file.file.read())
    except Exception as e:
        print("Error upload_file: ", e)
        raise HTTPException(status_code=400, detail=f"Error upload file, {e}")
    return {"url": url}


@router.delete(
    "/remove", dependencies=[Depends(deps.get_current_active_admin)], status_code=200
)
def remove_file(file_name: str, bucket: str = None):
    try:
        minio_services.delete_file(file_name, bucket=bucket)
    except Exception as e:
        print("Error remove_file: ", e)
        raise HTTPException(status_code=400, detail=f"Error remove file, {e}")
    return {"message": "Remove file successfully"}
