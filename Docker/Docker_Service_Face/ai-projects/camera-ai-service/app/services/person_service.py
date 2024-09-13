import json
import os
import threading
from datetime import datetime
from typing import List

import cv2
import face_recognition
import numpy as np
import requests
from fastapi import UploadFile, HTTPException

from app.common.convert_image import convert_image
from app.core.config import settings
from app.models.person_camera_model import PersonCamera
from app.models.person_model import Person
from app.schemas.person_image_schemas import PersonImageCreate
from app.schemas.person_schemas import (
    PersonCreate,
    PersonUpdate,
    PersonRegister,
    PersonModify,
)
from app.services.base_services import CRUDBase
from app.services.minio_services import MinioServices
from app.services.person_image_service import person_image_services


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    minio_services = MinioServices()

    async def check_image_valid(self, files: List[UploadFile]):
        images_success = []
        image_error = []
        image_crop = []
        images = []

        try:
            for file in files:
                contents = await file.read()
                nparr = np.frombuffer(contents, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                images.append(contents)
                # if (len(contents) / 1000) < 100:
                #     continue
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_image)
                if len(face_locations) == 1:
                    images_success.append(file.filename)
                    # x, y, w, h = faces[0]
                    # crop = image[y:y + h, x:x + w]
                    image_crop.append(image)
                else:
                    image_error.append(file.filename)

            if len(image_error) > 0:
                raise HTTPException(
                    status_code=400, detail={"code": "4536", "image_error": image_error}
                )
            return images

        except Exception as e:
            print("Error check image", e)
            raise HTTPException(
                status_code=400,
                detail={"code": "4536", "message": "Image is not valid"},
            )

    def check_info_other(self, other_info: str):
        other_info_dict = {}
        try:
            # Parse string to dict using json.loads()
            if other_info:
                other_info_dict = json.loads(other_info)
        except Exception:
            # Handle JSON decoding errors
            raise HTTPException(
                status_code=402, detail="other_info is not a valid JSON string"
            )
        return other_info_dict

    async def create_person(self, *, obj_in: PersonCreate, files: List[UploadFile]):
        images = await self.check_image_valid(files)
        data_save = super().create(obj_in=obj_in)
        # Save the images
        save_directory = "./temp"
        os.makedirs(save_directory, exist_ok=True)
        check = False
        list_image = []
        for contents in images:
            name = f"{data_save.id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            status = self.minio_services.upload_file_form(
                name, contents, bucket=settings.BUCKET_FACE
            )
            list_image.append({"name": name + ".jpg", "url": status})
            if status is False:
                check = True
                break

        if check:
            for image in list_image:
                self.minio_services.delete_file(
                    image["name"], bucket=settings.BUCKET_FACE
                )
            self.remove(id=str(data_save.id))
            raise HTTPException(
                status_code=400,
                detail={"code": "4537", "message": "Upload image failed"},
            )
        for image in list_image:
            image_create = {
                "person_id": str(data_save.id),
                "url": image["url"],
                "name": image["name"],
            }
            d = PersonImageCreate(**image_create)
            person_image_services.create(obj_in=d)

        return data_save

    def check_valid_image(self, data):
        list_bytes = []
        try:
            for item in data:
                response = requests.get(item)
                image_bytes = response.content
                image_bytes = convert_image(image_bytes)
                list_bytes.append(image_bytes)
                if image_bytes is False:
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "status": False,
                            "status_code": 404,
                            "message": "Register with no data face",
                        },
                    )
        except Exception:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": False,
                    "status_code": 404,
                    "message": "Register with no data face",
                },
            )

        return list_bytes

    def upload_image(self, id, data):
        save_directory = "./temp"
        os.makedirs(save_directory, exist_ok=True)
        check = False
        list_image = []
        for item in data:
            try:
                tim_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
                name = f"{id}_{tim_now}"
                crop_path = os.path.join(save_directory, name + ".jpg")
                response = requests.get(item)
                image_bytes = response.content
                # save image to file
                with open(crop_path, "wb") as file:
                    file.write(image_bytes)
                status = self.minio_services.upload_file(
                    crop_path, name + ".jpg", bucket=settings.BUCKET_FACE
                )
                list_image.append({"name": name + ".jpg", "url": status})
                if os.path.exists(crop_path):
                    os.remove(crop_path)
                if status is False:
                    check = True
                    break
            except Exception:
                check = True
                break
        return check, list_image

    def register_person(self, data: PersonRegister, id_company: str):
        if not data.name:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": False,
                    "status_code": 404,
                    "message": "Don't enough fields to register new user",
                },
            )
        if len(data.data) == 0:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": False,
                    "status_code": 404,
                    "message": "Don't enough fields to register new user",
                },
            )

        list_bytes = self.check_valid_image(data.data)  # noqa

        data_convert = {"name": data.name, "company_id": id_company, "other_info": {}}
        data_save = super().create(obj_in=PersonCreate(**data_convert))
        check, list_image = self.upload_image(data_save.id, data.data)
        if check:
            for image in list_image:
                self.minio_services.delete_file(
                    image["name"], bucket=settings.BUCKET_FACE
                )
            self.remove(id=str(data_save.id))
            raise HTTPException(
                status_code=404,
                detail={
                    "status": False,
                    "status_code": 404,
                    "message": "Don't enough fields to register new user",
                },
            )

        for image in list_image:
            image_create = {
                "person_id": str(data_save.id),
                "url": image["url"],
                "name": image["name"],
            }
            d = PersonImageCreate(**image_create)
            person_image_services.create(obj_in=d)
        from app.services.person_camera_services import person_camera_services

        threading.Thread(
            target=person_camera_services.create_multi_camera_user,
            args=(str(data_save.id), data.list_camera),
        ).start()
        # person_camera_services.create_multi_camera_user(id_company=id_company, person_id=str(data_save.id))

        return {
            "user_id": str(data_save.id),
            "status": True,
            "status_code": 200,
            "message": "Register successfully!",
        }

    def modifier_person(self, data: PersonModify, id_company: str):
        person = self.get(id=data.user_id)
        data_update = {}
        if not person:
            raise HTTPException(
                status_code=404,
                detail={
                    "status": False,
                    "status_code": 404,
                    "message": "User not found",
                },
            )
        self.check_valid_image(data.data)

        if data.name:
            data_update["name"] = data.name
        # if len(data.data) == 0:
        #     person_image_services.delete_by_person_id(id_person=data.user_id)

        if data.data:
            check, list_image = self.upload_image(data.user_id, data.data)
            if check:
                for image in list_image:
                    self.minio_services.delete_file(
                        image["name"], bucket=settings.BUCKET_FACE
                    )
                raise HTTPException(
                    status_code=404,
                    detail={
                        "status": False,
                        "status_code": 404,
                        "message": "Don't enough fields to register new user",
                    },
                )
            person_image_services.delete_by_person_id(id_person=data.user_id)
            list_image_create = []
            for image in list_image:
                image_create = {
                    "person_id": data.user_id,
                    "url": image["url"],
                    "name": image["name"],
                }
                d = PersonImageCreate(**image_create)
                person_image_services.create(obj_in=d)
                list_image_create.append(d)

        data_result = {}
        if data_update:
            data_result["data"] = self.update(
                obj_in=PersonUpdate(**data_update), db_obj=person
            )

        person_cameras = self.engine.find(
            PersonCamera, PersonCamera.person_id == str(data.user_id)
        )
        list_result = []
        for person_camera in person_cameras:
            list_result.append(
                {
                    "id_camera": str(person_camera.camera_id),
                    "type": person_camera.type_camera,
                    "id_person_camera": str(person_camera.id),
                }
            )
        data_result["person_camera"] = list_result
        return data_result

    def update_person(self, obj_in: PersonUpdate, id_person: str):
        person = self.get(id=id_person)
        if not person:
            raise HTTPException(status_code=400, detail="Person not found")

        return self.update(obj_in=obj_in, db_obj=person)

    def delete_person(self, id_person: str):
        person = self.get(id=id_person)
        if not person:
            raise HTTPException(status_code=400, detail="Person not found")
        list_person_camera = list(
            self.engine.find(PersonCamera, PersonCamera.person_id == id_person)
        )
        list_camera_person = []
        for person_camera in list_person_camera:
            list_camera_person.append(
                {
                    "id_camera": person_camera.camera_id,
                    "id_person_camera": str(person_camera.id),
                    "type": person_camera.type_camera,
                }
            )
        self.remove(id=id_person)
        person_image_services.delete_by_person_id(id_person=id_person)
        return {"data": person, "list_camera_person": list_camera_person}

    def get_person_by_company(
        self,
        id_company: str,
        page: int = 0,
        page_break: bool = False,
        data_search: str = None,
    ):
        offset = {"skip": page * 20, "limit": 20} if page_break else {}
        persons = None
        if data_search:
            regex_query = {"name": {"$regex": data_search, "$options": "i"}}
            persons = self.engine.find(
                Person,
                Person.company_id == id_company,
                {"$and": [regex_query, {"company_id": id_company}]},
                **offset,
                sort=self.model.created.desc(),
            )
        else:
            persons = self.engine.find(
                Person,
                Person.company_id == id_company,
                **offset,
                sort=self.model.created.desc(),
            )
        list_person = []
        for person in persons:
            person_id = str(person.id)
            images = person_image_services.get_image_by_person_id(person_id=person_id)
            list_image = []
            for image in images:
                list_image.append(
                    {"id": str(image.id), "url": image.url, "name": image.name}
                )
            data = {}
            for key, value in person.dict().items():
                if key == "id":
                    data["id"] = str(value)
                else:
                    data[key] = value
            data["images"] = list_image
            list_person.append(data)

        return list_person

    def get_person_by_company_camera(
        self,
        id_company: str,
        id_camera: str,
        page: int = 0,
        page_break: bool = False,
        data_search: str = None,
        filter: str = None,
    ):
        list_person = []
        filter_setting = {"$match": {}}
        if filter == "NO_SETTING":
            filter_setting = {
                "$match": {
                    "cameras.camera_id": {
                        "$ne": id_camera
                    }  # Lọc theo điều kiện camera_id == "1"
                }
            }
        if filter == "SETTING":
            filter_setting = {
                "$match": {
                    "cameras.camera_id": {
                        "$eq": id_camera
                    }  # Loại bỏ các document có camera_id bằng "1"
                }
            }
        search = {"$match": {}}
        if data_search:
            search = {
                "$match": {
                    "$or": [
                        {"name": {"$regex": data_search, "$options": "i"}},
                    ]
                }
            }

        pipeline = [
            {
                "$addFields": {
                    "_id_str": {"$toString": "$_id"}  # Chuyển đổi ObjectId sang string
                }
            },
            {
                "$lookup": {
                    "from": "person_camera",
                    "localField": "_id_str",
                    "foreignField": "person_id",
                    "as": "cameras",
                }
            },
            {
                "$lookup": {
                    "from": "person_image",
                    "localField": "_id_str",
                    "foreignField": "person_id",
                    "as": "images",
                }
            },
            {"$match": {"company_id": id_company}},
            filter_setting,
            search,
            {"$sort": {"created": -1}},
            {"$skip": page * 20},
            {"$limit": 20},
            {
                "$group": {
                    "_id": {"$toString": "$_id"},
                    "name": {"$first": "$name"},
                    "other_info": {"$first": "$other_info"},
                    "created": {"$first": "$created"},
                    "images": {"$push": "$images"},
                    "cameras": {"$push": "$cameras"},
                }
            },
            {"$project": {"_id_str": 0}},
        ]
        data = self.engine.get_collection(Person).aggregate(pipeline)

        data = list(data)
        for i in data:
            images = i["images"]
            cameras = i["cameras"]
            list_image = []
            for image in images:
                for i2 in image:
                    list_image.append(
                        {"id": str(i2["_id"]), "url": i2["url"], "name": i2["name"]}
                    )
            is_supervision = False
            id_person_camera = None
            for camera in cameras:
                for i3 in camera:
                    if str(i3["camera_id"]) == id_camera:
                        is_supervision = True
                        id_person_camera = str(i3["_id"])
                        break
                if is_supervision:
                    break
            i["images"] = list_image
            i["id_person_camera"] = id_person_camera
            del i["cameras"]
            i["is_supervision"] = is_supervision
            i["id"] = i["_id"]
            del i["_id"]
            list_person.append(i)

        return list_person

    def get_count_person_by_company_camera(
        self,
        id_company: str,
        id_camera: str,
        data_search: str = None,
        filter: str = None,
    ):
        filter_setting = {"$match": {}}
        if filter == "NO_SETTING":
            filter_setting = {
                "$match": {
                    "cameras.camera_id": {
                        "$ne": id_camera
                    }  # Lọc theo điều kiện camera_id == "1"
                }
            }
        if filter == "SETTING":
            filter_setting = {
                "$match": {
                    "cameras.camera_id": {
                        "$eq": id_camera
                    }  # Loại bỏ các document có camera_id bằng "1"
                }
            }
        search = {"$match": {}}
        if data_search:
            search = {
                "$match": {
                    "$or": [
                        {"name": {"$regex": data_search, "$options": "i"}},
                    ]
                }
            }

        pipeline = [
            {
                "$addFields": {
                    "_id_str": {"$toString": "$_id"}  # Chuyển đổi ObjectId sang string
                }
            },
            {
                "$lookup": {
                    "from": "person_camera",
                    "localField": "_id_str",
                    "foreignField": "person_id",
                    "as": "cameras",
                }
            },
            {
                "$lookup": {
                    "from": "person_image",
                    "localField": "_id_str",
                    "foreignField": "person_id",
                    "as": "images",
                }
            },
            {"$match": {"company_id": id_company}},
            filter_setting,
            search,
            {
                "$group": {
                    "_id": {"$toString": "$_id"},
                    "name": {"$first": "$name"},
                    "created": {"$first": "$created"},
                    "images": {"$push": "$images"},
                    "cameras": {"$push": "$cameras"},
                }
            },
            {"$project": {"_id_str": 0}},
        ]
        data = self.engine.get_collection(Person).aggregate(pipeline)
        return len(list(data))

    def async_user(self, id_company: str):
        persons = self.engine.find(Person, Person.company_id == id_company)
        list_person = []
        for person in persons:
            person_id = str(person.id)
            images = person_image_services.get_image_by_person_id(person_id=person_id)
            list_image = []
            for image in images:
                list_image.append(image.url)
            data = {}
            for key, value in person.dict().items():
                if key == "id":
                    data["id"] = str(value)
                else:
                    data[key] = value
            data_send = {
                "name": data["name"],
                "user_id": data["id"],
                "type": None,
                "created_at": data["created"],
                "url_ori": list_image,
            }
            list_person.append(data_send)
        return list_person

    def get_count_by_company(self, id_company: str, data_search: str = None):
        if data_search:
            regex_query = {"name": {"$regex": data_search, "$options": "i"}}
            count = self.engine.count(
                Person,
                Person.company_id == id_company,
                {"$and": [regex_query, {"company_id": id_company}]},
            )
        else:
            count = self.engine.count(Person, Person.company_id == id_company)
        return count

    def get_by_id(self, id: str):
        return self.get(id=id)

    def get_by_person_id_camera(self, person_id_camera: str):
        data = self.engine.find_one(
            PersonCamera, PersonCamera.person_id_camera == person_id_camera
        )
        if data:
            return self.get(id=data.person_id)
        return None


person_services = CRUDPerson(Person)
