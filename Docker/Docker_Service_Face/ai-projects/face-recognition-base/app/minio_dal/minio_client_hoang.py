import traceback

from minio import Minio
from datetime import datetime
from datetime import timedelta

from sentry_sdk import capture_exception, capture_message

from app.app_utils.file_io_untils import ip_run_service_ai

# from settings.config import BUCKET_NAME, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY


minio_endpoint = 's3.oryza.vn'
minio_access_key = 'hoang'
minio_secret_key = '12345678'

minio_client = Minio(
    endpoint=minio_endpoint,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False
)

bucket_name = 'vms-plugin'


class MinioClient:
    def __init__(self):
        self.minio_client = minio_client
        self.bucket_name = bucket_name

    def get_object_one(self, file_name):
        url = self.minio_client.presigned_get_object(bucket_name, file_name)
        return url

    def list_obj(self, arr_list):
        rs = []
        for _ in arr_list:
            url = self.minio_client.presigned_get_object(bucket_name, _)
            rs.append(url)
        return rs

    def create_obj(self, file, filename, content_type, size):
        try:
            self.minio_client.put_object(bucket_name, filename, file, size, content_type)
            url_link = self.minio_client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=filename
            )
            return True, url_link
        except Exception as e:
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")
            return False, str(e)

    def delete_obj(self, filename):
        try:
            self.minio_client.remove_object(bucket_name, filename)
            return {
                "status": "success",
                "message": "Delete file success",
                "data": {
                    "file_name": filename,
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Delete file error",
                "data": str(e)
            }

    def delete_list_obj(self, list_obj):
        try:
            for _ in list_obj:
                self.minio_client.remove_object(bucket_name, f'face_db/{_}.jpg')
            return {
                "status": "success",
                "message": "Delete file success",
                "data": {
                    "file_name": list_obj,
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Delete file error",
                "data": str(e)
            }
