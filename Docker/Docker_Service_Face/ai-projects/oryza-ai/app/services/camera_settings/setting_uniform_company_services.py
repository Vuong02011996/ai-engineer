import ast
import uuid
from datetime import datetime
from typing import List

import requests
from fastapi import HTTPException
from odmantic import ObjectId
from starlette.datastructures import UploadFile

from app.common.constants.rabbitmq_constants import IDENTIFY_UNIFORMS_EXCHANGES
from app.common.utils.minio_services import MinioServices
from app.models import User, Service, TypeService
from app.models.camera_settings.setting_uniforms_conpany import SettingUniformsCompany
from app.schemas.camera_settings.setting_uniforms_company import SettingUniformsCompanyCreate, \
    SettingUniformsCompanyUpdate
from app.services.base_services import CRUDBase
from app.services.process_services import service_services


class SettingUniformsCompanyServie(
    CRUDBase[
        SettingUniformsCompany, SettingUniformsCompanyCreate, SettingUniformsCompanyUpdate
    ]
):
    async def create_setting(self, files: List[UploadFile], rgb: str, user: User):
        self.check_rgb(rgb)
        setting_exist = self.get_by_id_company(id_company=str(user.company.id))

        if setting_exist:
            raise HTTPException(status_code=400, detail="Setting already exists")

        minio_services = MinioServices()
        list_image = []
        list_name = []

        if files is not None:

            for file in files:
                name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                name += uuid.uuid4().hex
                list_name.append("setting_uniforms_company/" + name)

                file_content = await file.read()
                url = minio_services.upload_file_form(name=name, contents=file_content,
                                                      forder="setting_uniforms_company")
                if url is False:
                    # delete all image
                    for i in list_name:
                        minio_services.delete_file(i)
                    raise HTTPException(status_code=400, detail="Error upload image")
                list_image.append(url)
        setting = SettingUniformsCompanyCreate(
            rgb=rgb,
            id_company=str(user.company.id),
            list_image=list_image
        )
        data = self.create(obj_in=setting)
        self.create_from_sub_service(setting=setting_exist)
        return data

    def create_from_sub_service(self, setting: SettingUniformsCompany, ip_address: str = None, port: int = None):
        try:
            service = service_services.get_info_by_key(IDENTIFY_UNIFORMS_EXCHANGES)
            if not service:
                return False
            if not ip_address or not port:
                ip_address = service.server.ip_address
                port = service.port
            url = f"http://{ip_address}:{port}/set_config"
            list_image = []
            if setting.list_image:
                list_image = setting.list_image
            data = {
                "company_id": setting.id_company,
                "rgb": setting.rgb,
                "image_urls": list_image
            }
            response = requests.post(url, json=data)
            if response.status_code != 200 and response.status_code != 201:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def get_by_id_company(self, id_company: str):
        return self.engine.find_one(SettingUniformsCompany, SettingUniformsCompany.id_company == id_company)

    def check_rgb(self, rgb: str):
        try:
            array = ast.literal_eval(rgb)
            if len(array) != 3:
                raise HTTPException(status_code=400, detail="Mã màu không đúng định dạng")
            for i in array:
                if i < 0 or i > 255:
                    raise HTTPException(status_code=400, detail="Mã màu không đúng định dạng")
        except:
            raise HTTPException(status_code=400, detail="Mã màu không đúng định dạng")

    def update_setting(self, id: str, obj_in: SettingUniformsCompanyUpdate):
        self.check_rgb(obj_in.rgb)
        setting = self.get(id)
        if not setting:
            raise HTTPException(status_code=400, detail="Setting not found")
        data = self.update(db_obj=setting, obj_in=obj_in)
        self.create_from_sub_service(setting=setting)
        return data

    def update_image(self, id: str, image: UploadFile):
        setting = self.get(id)
        if not setting:
            raise HTTPException(status_code=400, detail="Setting not found")
        minio_services = MinioServices()
        file_content = image.file.read()
        name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        name += uuid.uuid4().hex
        url = minio_services.upload_file_form(name=name, contents=file_content,
                                              forder="setting_uniforms_company")
        if url is False:
            raise HTTPException(status_code=400, detail="Error upload image")
        setting.list_image.append(url)
        self.engine.save(setting)
        self.create_from_sub_service(setting=setting)
        return setting

    def delete_image(self, id: str, image_id: str):
        setting = self.get(id)
        if not setting:
            raise HTTPException(status_code=400, detail="Setting not found")
        setting.list_image = [i for i in setting.list_image if i != image_id]
        self.engine.save(setting)
        minio_services = MinioServices()
        array = image_id.split("/")
        image_id = "setting_uniforms_company/" + array[-1]
        minio_services.delete_file(image_id)
        self.create_from_sub_service(setting=setting)
        return setting

    def delete(self, user: User):
        setting = self.get_by_id_company(str(user.company.id))
        if not setting:
            raise HTTPException(status_code=400, detail="Setting not found")
        # delete all image
        for i in setting.list_image:
            self.delete_image(id=id, image_id=i)
        self.engine.delete(setting)
        return setting


setting_uniform_company_services = SettingUniformsCompanyServie(SettingUniformsCompany)
