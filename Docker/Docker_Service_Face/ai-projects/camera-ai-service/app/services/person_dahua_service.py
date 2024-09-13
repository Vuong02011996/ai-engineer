import uuid

from fastapi import HTTPException

from app.common.send_request_camera_dahua import perform_digest_authentication
from app.common.utils import clean_update_input
from app.schemas.person_dahua_schema import (
    CreatePerson,
    UpdatePerson,
    DeletePerson,
    OutsPerson,
)


class PersonDahuaService:
    def create_preson(self, new_data: CreatePerson):
        data_params = ""
        if new_data.sex:
            data_params += f"&sex={new_data.sex}"
        if new_data.birthday:
            data_params += f"&birthday={new_data.birthday}"
        if new_data.country:
            data_params += f"&country={new_data.country}"
        if new_data.city:
            data_params += f"&city={new_data.city}"
        ID = str(uuid.uuid4().hex)[:30]
        ID = str.replace(ID, "-", "")
        data_params += f"&id={ID}"

        url = f"http://{new_data.host}/cgi-bin/faceRecognitionServer.cgi?action=addPerson&groupID={new_data.group_id}&name={new_data.name}{data_params}"

        try:
            # print(url, new_data.username, new_data.password)
            text_response = perform_digest_authentication(
                url=url,
                method="POST",
                username=new_data.username,
                password=new_data.password,
                image=new_data.image,
            )

            return text_response

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating group {e}")

    def update_person(self, update_data: UpdatePerson):
        update_data = clean_update_input(update_data)
        data_send = ""
        if update_data.get("name"):
            data_send += f"&name={update_data.get('name')}"
        if update_data.get("sex"):
            data_send += f"&sex={update_data.get('sex')}"
        if update_data.get("birthday"):
            data_send += f"&birthday={update_data.get('birthday')}"
        if update_data.get("country"):
            data_send += f"&country={update_data.get('country')}"
        if update_data.get("city"):
            data_send += f"&city={update_data.get('city')}"
        if data_send == "" and not update_data.get("image"):
            raise HTTPException(status_code=400, detail="No data to update")
        url = f'http://{update_data.get("host")}/cgi-bin/faceRecognitionServer.cgi?action=modifyPerson&groupID={update_data.get("group_id")}&uid={update_data.get("uid")}{data_send}'
        try:
            text_response = perform_digest_authentication(
                url=url,
                method="POST",
                username=update_data.get("username"),
                password=update_data.get("password"),
                image=update_data.get("image"),
            )
            return text_response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating group {e}")

    def delete_person(self, delete_data: DeletePerson):
        url = f"http://{delete_data.host}/cgi-bin/faceRecognitionServer.cgi?action=deletePerson&groupID={delete_data.group_id}&uid={delete_data.uid}"
        try:
            text_response = perform_digest_authentication(
                url=url,
                method="GET",
                username=delete_data.username,
                password=delete_data.password,
            )
            return text_response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error deleting group {e}")

    def convert_to_json(self, text):
        if not text:
            return None
        text = text.split("\r\n")
        data = {}
        for i in text:
            if "=" in i:
                t = i.split("=")
                if len(t) != 2:
                    continue
                key = t[0]
                data[key] = t[1]
        return data

    def get_all(self, data: OutsPerson):
        url = f"http://{data.host}/cgi-bin/faceRecognitionServer.cgi?action=startFind&condition.GroupID[0]={data.group_id}"
        try:
            text_response = perform_digest_authentication(
                url=url, method="GET", username=data.username, password=data.password
            )
            data_token = self.convert_to_json(text_response)
            if (
                not data_token
                or "token" not in data_token
                or "totalCount" not in data_token
            ):
                raise HTTPException(status_code=404, detail="Group not found")
            data_res = []
            data_token["data"] = []
            start = data.page * 10
            end = start + 1
            total = int(data_token["totalCount"])

            if start > total:
                return data_token
            if end > total:
                end = total

            for i in range(start, end):
                url = f'http://{data.host}/cgi-bin/faceRecognitionServer.cgi?action=doFind&token={data_token["token"]}&index={i}'
                text_response = perform_digest_authentication(
                    url=url,
                    method="GET",
                    username=data.username,
                    password=data.password,
                )
                arr_text = text_response.split("--myboundary")
                if len(arr_text) < 2:
                    continue
                data_res.append(self.convert_to_json(arr_text[1]))
            url = f'http://{data.host}/cgi-bin/faceRecognitionServer.cgi?action=stopFind&token={data_token["token"]}'
            text_response = perform_digest_authentication(
                url=url, method="GET", username=data.username, password=data.password
            )
            data_token["data"] = data_res
            return data_token

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting all person {e}")


person_dahua_service = PersonDahuaService()
