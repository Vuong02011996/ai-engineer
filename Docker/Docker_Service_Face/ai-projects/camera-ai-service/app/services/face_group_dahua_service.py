from fastapi import HTTPException

from app.common.send_request_camera_dahua import perform_digest_authentication
from app.common.utils import clean_update_input, text_to_object
from app.schemas.base_face_camera_dahua import BaseCameraDahua
from app.schemas.face_group_dahua_schema import CreateFaceGroup, UpdateFaceGroup, DeleteFaceGroup


class FaceGroupDahuaService():
    def create_face_group(self, new_data: CreateFaceGroup):
        if not new_data.group_name or new_data.group_name.strip() == "":
            raise HTTPException(status_code=400, detail="Group name is required")
        if not new_data.group_detail:
            new_data.group_detail = ""
        url = f'http://{new_data.host}/cgi-bin/faceRecognitionServer.cgi?action=createGroup&groupName={new_data.group_name}&groupDetail={new_data.group_detail}'
        try:
            text_response = perform_digest_authentication(url=url, method="GET", username=new_data.username,
                                                          password=new_data.password)

            return text_response

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating group {e}")

    def update_face_group(self, update_data: UpdateFaceGroup):
        update_data = clean_update_input(update_data)
        data_send = ""
        if update_data.get("group_name"):
            data_send += f"&groupName={update_data.get('group_name')}"
        if update_data.get("group_detail"):
            data_send += f"&groupDetail={update_data.get('group_detail')}"
        if data_send == "":
            raise HTTPException(status_code=400, detail="No data to update")
        url = f'http://{update_data.get("host")}/cgi-bin/faceRecognitionServer.cgi?action=modifyGroup&groupID={update_data.get("group_id")}&{data_send}'

        try:

            text_response = perform_digest_authentication(url=url, method="GET", username=update_data.get("username"),
                                                          password=update_data.get("password"))
            return text_response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating group {e}")

    def delete_face_group(self, delete_data: DeleteFaceGroup):
        url = f'http://{delete_data.host}/cgi-bin/faceRecognitionServer.cgi?action=deleteGroup&groupID={delete_data.group_id}'
        try:
            text_response = perform_digest_authentication(url=url, method="GET", username=delete_data.username,
                                                          password=delete_data.password)
            return text_response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error deleting group {e}")

    def get_all(self, data: BaseCameraDahua):
        print(data.host, data.username, data.password)
        url = f'http://{data.host}/cgi-bin/faceRecognitionServer.cgi?action=findGroup'
        try:
            text_response = perform_digest_authentication(url=url, method="GET", username=data.username,
                                                          password=data.password)
            return text_to_object(text_response)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting all group {e}")




face_group_dahua_service = FaceGroupDahuaService()
