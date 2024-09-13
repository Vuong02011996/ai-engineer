from requests.auth import HTTPDigestAuth
import requests
import time
import random
import xml.etree.ElementTree as ET

from app.core.config import settings
from app.schemas.person_hik_schemas import (
    GetPersonCameraHik as GetPerson,
    CreatePersonCameraHik as CreatePerson,
    DeletePersonCameraHik as DeletePerson,
    UpdateImagePersonCameraHik as UpdateImagePerson,
    UpdateInfoPersonCameraHik as UpdateInfoPerson,
)


class PersonHikService:
    """Service to interact with Hikvision camera. Include get, create, delete person."""

    def create_facelib(
        self, address: str, username: str, password: str, threshold: int = 60
    ):
        """Create facelib 1 in the camera."""
        url = f"http://{address}/ISAPI/Intelligent/FDLib"
        auth = HTTPDigestAuth(username, password)
        # threshold = 60
        xml = f"<CreateFDLibList><CreateFDLib><name>1</name><thresholdValue>{threshold}</thresholdValue></CreateFDLib></CreateFDLibList>"
        try:
            # print("url", url)
            response = requests.post(
                url,
                auth=auth,
                data=xml,
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                print("Create facelib successfully")
                root = ET.fromstring(response.content)
                first_id_element = root.find(
                    "{http://www.hikvision.com/ver20/XMLSchema}FDLibInfo/{http://www.hikvision.com/ver20/XMLSchema}id"
                )
                if first_id_element is not None:
                    return str(first_id_element.text)
                else:
                    print("No id found in the response")
            else:
                print("Failed to create facelib, status code:", response.status_code)
        except Exception as e:
            print(f"Error call to camera in create facelib 1: {e}")
            return False

    def get_first_facelib_id(self, address: str, username: str, password: str):
        """Get the first facelib in the camera. If not exist, create one."""

        # for testing. Uncomment and the return below to return the second facelib
        # return "2"

        url = f"http://{address}/ISAPI/Intelligent/FDLib"
        auth = HTTPDigestAuth(username, password)
        try:
            response = requests.get(
                url,
                auth=auth,
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                first_id = root.find(
                    "{http://www.hikvision.com/ver20/XMLSchema}FDLibBaseCfg/{http://www.hikvision.com/ver20/XMLSchema}id"
                )
                if first_id is not None:
                    return str(first_id.text)
                else:
                    # No FDLibBaseCfg elements found, create one
                    return self.create_facelib(address, username, password)
            else:
                print(
                    f"Error call to camera in get facelib 1, camera response: {response.text}"
                )
                return False
        except Exception as e:
            print(f"Error call to camera in get facelib 1: {e}")
            return False

    def get_person(self, data: GetPerson):
        """Get a person in the Hikvision camera by pid. Return the name."""
        facelib_id = self.get_first_facelib_id(
            data.address, data.username, data.password
        )
        # print("pid", data.pid)
        url = f"http://{data.address}/ISAPI/Intelligent/FDLib/{facelib_id}/picture/{data.pid}"
        auth = HTTPDigestAuth(data.username, data.password)

        try:
            response = requests.get(
                url,
                auth=auth,
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                name = root.find("{http://www.hikvision.com/ver20/XMLSchema}name").text
                custom_pid = root.find(
                    "{http://www.hikvision.com/ver20/XMLSchema}certificateNumber"
                ).text
                return name, custom_pid
            else:
                print(
                    f"Error call to camera in get person, camera response: {response.text}"
                )
                return None
        except Exception as e:
            print(f"Error call to camera in get person: {e}")
            return None

    def create_person(self, data: CreatePerson):
        """Create a person in the Hikvision camera. Return the PID."""
        facelib_id = self.get_first_facelib_id(
            data.address, data.username, data.password
        )
        # If this function use when update image, custom_pid is not None.
        # The logic is to create a new person with the same name and custom_pid
        # then delete the old person.

        # Otherwise, create a new person with a new custom_pid.
        # Max bit of custom_pid is 32. Dont try to use uuid
        if data.custom_pid is None:
            custom_pid = str(int(time.time())) + str(random.randint(10, 99))
        else:
            custom_pid = data.custom_pid
        url = f"http://{data.address}/ISAPI/Intelligent/FDLib/{facelib_id}/picture"
        auth = HTTPDigestAuth(data.username, data.password)

        xml = f'<?xml version="1.0" encoding="UTF-8"?><FaceAppendData><name>{data.name}</name><certificateNumber>{custom_pid}</certificateNumber></FaceAppendData>'
        payload = {"FaceAppendData": xml}
        files = [
            ("importImage", (f"{custom_pid}.jpg", data.image, "image/jpeg"))
        ]  # filename is whatever you want

        try:
            response = requests.post(
                url,
                auth=auth,
                data=payload,
                files=files,
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                pid = root.find("{http://www.hikvision.com/ver20/XMLSchema}PID").text
                print(f"Create person pid={pid} successfully")
                return pid, custom_pid
                # We still collect pid, but the camera often mess up the pid, so we use custom_pid instead
            else:
                print(
                    f"Error call to camera in create person, camera response: {response.text}"
                )
                return None
        except Exception as e:
            print(f"Error call to camera in create person: {e}")
            return None

    def delete_person(self, data: DeletePerson):
        """Delete a person in the Hikvision camera by pid."""
        # Check if person exist
        name, custom_id = self.get_person(GetPerson(**data.model_dump()))
        if name is None and custom_id is None:
            print("Person is not exist in camera")
            return True

        facelib_id = self.get_first_facelib_id(
            data.address, data.username, data.password
        )
        url = f"http://{data.address}/ISAPI/Intelligent/FDLib/{facelib_id}/picture/{data.pid}"
        auth = HTTPDigestAuth(data.username, data.password)
        try:
            response = requests.delete(
                url,
                auth=auth,
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                print(f"Delete person pid={data.pid} successfully")
                return True
            else:
                print(
                    f"Error call to camera in delete person, camera response: {response.text}"
                )
                return False
        except Exception as e:
            print(f"Error call to camera in delete person: {e}")
            return False

    def update_image_person(self, update_data: UpdateImagePerson):
        from app.services.person_camera_services import person_camera_services

        """
        1. Get the person with the PID, get the name
        2. Delete the person with the PID
        3. Create a new person with name from 1, get the new PID
        4. Update pid of person in database by the new PID (outside of this function)
        """
        data = update_data.model_dump()
        name, custom_id = self.get_person(GetPerson(**data))
        if name is None or custom_id is None:
            print("Imange is not exist in camera, let's create new person")
            data["name"] = data["pid"]
        else:
            # double check with database, if match, delete person
            person_cameras = person_camera_services.get_by_person_id_camera(data["pid"])
            print("person_cameras", person_cameras)
            for camera in person_cameras:
                if camera.person_id_camera == custom_id:
                    try:
                        self.delete_person(DeletePerson(**data))
                    except Exception as e:
                        print("Error delete person", e)
                        continue
            data["name"] = name
            data["custom_id"] = custom_id

        new_pid, custom_id = self.create_person(CreatePerson(**data))
        print("new_pid", new_pid, "custom_id", custom_id)
        return new_pid, custom_id

    def update_info_person(self, update_data: UpdateInfoPerson):
        """Update the name of a person in the Hikvision camera by pid."""
        facelib_id = self.get_first_facelib_id(
            update_data.address, update_data.username, update_data.password
        )
        url = f"http://{update_data.address}/ISAPI/Intelligent/FDLib/{facelib_id}/picture/{update_data.pid}"
        auth = HTTPDigestAuth(update_data.username, update_data.password)
        xml = f'<?xml version="1.0" encoding="UTF-8"?><FaceAppendData><name>{update_data.name}</name></FaceAppendData>'
        payload = {"FaceAppendData": xml}
        try:
            response = requests.put(
                url,
                auth=auth,
                data=payload,
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                print(f"Update person pid={update_data.pid} successfully")
                return True
            else:
                print(
                    f"Error call to camera in update person, camera response: {response.text}"
                )
                return False
        except Exception as e:
            print(f"Error call to camera in update person: {e}")
            return False


person_hik_services = PersonHikService()
