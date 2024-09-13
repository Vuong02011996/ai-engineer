import requests
from requests.auth import HTTPDigestAuth
import json
import uuid
from app.core.config import settings
from app.schemas.person_access_control_schemas import (
    CreatePersonCameraAccessControl as CreatePerson,
    DeletePersonCameraAccessControl as DeletePerson,
    UpdateImagePersonCameraAccessControl as UpdateImagePerson,
)
from app.common.convert_image import convert_image_base64_downsize as convert_image
from datetime import datetime, timedelta


class PersonAccessControlServices:
    """
    Create, Update, Delete person in camera dahua access control
    """

    def create_person(self, rq: CreatePerson):
        """
        Create person in camera dahua access control
        1. Create user
        2. Add face to user
        To debug, see temp/add_user_payload.txt and temp/new_img.jpg
        """
        # Create user, use uuid as user_id and card_no, so that if the user failed to be deleted in the future,
        # it won't affect the creation of the new user
        id = str(uuid.uuid4())
        card_no = id[:16]
        user_id = id[:16]
        time_now = (
            datetime.now().strftime("%Y%m%d")
            + "%20"
            + datetime.now().strftime("%H%M%S")
        )
        five_years_later = (
            (datetime.now() + timedelta(days=1825)).strftime("%Y%m%d")
            + "%20"
            + (datetime.now() + timedelta(days=1825)).strftime("%H%M%S")
        )
        print("time_now", time_now)
        print("five_years_later", five_years_later)
        url = [
            f"http://{rq.address}/cgi-bin/recordUpdater.cgi",
            "?action=insert",
            "&name=AccessControlCard",
            f"&CardName={rq.person_name}",
            f"&CardNo={card_no}",
            f"&UserID={user_id}",
            "&CardStatus=0",
            "&Doors[0]=0",
            # "&Doors[1]=3",
            # "&Doors[2]=5",
            f"&ValidDateStart={time_now}",
            f"&ValidDateEnd={five_years_later}",
        ]
        url = "".join(url).replace(" ", "")
        print("1. Create user url", url)
        try:
            response = requests.get(
                url,
                auth=HTTPDigestAuth(rq.username, rq.password),
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code != 200:
                print("Create user failed")
                return None
        except requests.exceptions.Timeout:
            print("Access control camera add user timeout error")
            return None
        recno = str(response.text.split("RecNo=")[1].strip())
        print("Create user success", recno)

        # Add face to user
        url = f"""http://{rq.address}/cgi-bin/FaceInfoManager.cgi?action=add"""
        print("2. Add face url", url)
        ## Convert image to base64
        base64_image = convert_image(rq.image, 100)
        # with open(f"temp/new_{user_id}.jpg", "wb") as f:
        #     f.write(base64.b64decode(base64_image))

        body = {"UserID": user_id, "Info": {"PhotoData": [base64_image]}}
        with open("temp/add_user_payload.txt", "w") as f:
            f.write(str(body).replace("'", '"'))

        try:
            response = requests.post(
                url,
                auth=HTTPDigestAuth(rq.username, rq.password),
                data=json.dumps(body),
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code != 200:
                print("Add face failed")
                # Delete user if add face failed
                self.delete_person(DeletePerson(**rq.model_dump(), recno=recno))
                return None
        except requests.exceptions.Timeout:
            print("Timeout error")
            # Delete user if add face failed
            self.delete_person(DeletePerson(**rq.model_dump(), recno=recno))
            return None
        except Exception as e:
            print("[on cam] Error creating person access control", e)
            # Delete user if add face failed
            self.delete_person(DeletePerson(**rq.model_dump(), recno=recno))
            return None

        return recno, user_id

    def delete_person(self, rq: DeletePerson):
        url = f"http://{rq.address}/cgi-bin/recordUpdater.cgi?action=remove&name=AccessControlCard&recno={rq.recno}"
        print("Delete person url", url)
        try:
            response = requests.get(
                url,
                auth=HTTPDigestAuth(rq.username, rq.password),
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code != 200:
                print("Delete person on camera access control failed")
                print(response.text)
                return None
        except requests.exceptions.Timeout:
            print("Timeout error")
            return None
        except Exception as e:
            print("Error deleting person on camera access control", e)
            return None
        print("Delete person on camera access control success")

    def update_image_person(self, rq: UpdateImagePerson):
        url = f"http://{rq.address}/cgi-bin/FaceInfoManager.cgi?action=update"
        print("Update image person url", url)
        base64_image = convert_image(rq.image, 100)
        print(base64_image[:100])
        payload = {"UserID": rq.user_id, "Info": {"PhotoData": [base64_image]}}
        print("Update image person payload", json.dumps(payload)[:100])
        try:
            response = requests.post(
                url,
                auth=HTTPDigestAuth(rq.username, rq.password),
                data=json.dumps(payload),
                timeout=settings.REQUEST_TIMEOUT,
            )
            if response.status_code != 200:
                print("Update image person failed")
                return None
        except requests.exceptions.Timeout:
            print("Timeout error")
            return None
        except Exception as e:
            print("Error updating image person camera access control", e)
            return None


person_access_control_services = PersonAccessControlServices()
