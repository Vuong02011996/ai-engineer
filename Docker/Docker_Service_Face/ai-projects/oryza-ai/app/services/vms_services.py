import requests
from fastapi import HTTPException
from app.services.base_services import CRUDBase
from app.models.vms_model import VMS
from app.schemas.vms_schemas import VMSCreate, VMSUpdate, VMSCreateInDB, LoginInfo
from app.models import User, Company
from app.common.constants.enums import VmsTypeEnum


class CRUDVMS(CRUDBase[VMS, VMSCreate, VMSUpdate]):
    def get_by_id(self, *, id: str):
        vms = super().get(id)
        if not vms:
            raise HTTPException(status_code=404, detail="VMS not found")
        return vms

    def get_by_company_id(self, *, company_id: str):
        vms = self.engine.find_one(VMS, VMS.company_id == company_id)
        if not vms:
            raise HTTPException(status_code=404, detail="VMS not found")
        return vms

    def get_my_company_vms(self, *, user: User):
        vms = self.get_my_company_vms_raw(user=user)
        if not vms:
            raise HTTPException(status_code=404, detail="VMS not found")
        return vms

    def get_my_company_vms_raw(self, *, user: User):
        company_id = str(user.company.id)
        return self.engine.find_one(VMS, VMS.company_id == company_id)

    def get_vms_all(self):
        return super().get_multi()

    def count_vms(self):
        return super().count()

    def create_vms(self, *, user: User, obj_in: VMSCreate):
        # Check if vms already exists
        old_vms = self.get_my_company_vms_raw(user=user)
        # if vms:
        #     raise HTTPException(status_code=400, detail="VMS already exists")

        company: Company = user.company
        obj_create = obj_in.model_dump()
        obj_create["company_id"] = str(company.id)

        to_create_vms = VMSCreateInDB(**obj_create)
        login_info = LoginInfo(**to_create_vms.model_dump())
        # Check if auth info is correct
        self.login_vms(login_info)
        super().create(obj_in=to_create_vms)
        # Remove old vms
        if old_vms:
            self.remove_vms(id=str(old_vms.id))

    def update_my_company_vms(self, *, user: User, obj_in: VMSUpdate):
        vms = self.get_my_company_vms(user=user)
        return self.update_vms(to_update_vms=vms, obj_in=obj_in)

    def update_by_id(self, *, id: str, obj_in: VMSUpdate):
        vms: VMS = self.get_by_id(id=id)
        return self.update_vms(to_update_vms=vms, obj_in=obj_in)

    def update_vms(self, *, to_update_vms: VMS, obj_in: VMSUpdate):
        # Check if url already used
        duplicate_vms = self.engine.find_one(
            VMS,
            VMS.ip_address == obj_in.ip_address,
        )
        if duplicate_vms and duplicate_vms.id != to_update_vms.id:
            if obj_in.port and duplicate_vms.port and obj_in.port == duplicate_vms.port:
                raise HTTPException(status_code=400, detail="URL already used")
        # Check if auth info is correct
        login_info = LoginInfo(
            username=obj_in.username if obj_in.username else to_update_vms.username,
            password=obj_in.password if obj_in.password else to_update_vms.password,
            port=obj_in.port if obj_in.port else to_update_vms.port,
            ip_address=obj_in.ip_address
            if obj_in.ip_address
            else to_update_vms.ip_address,
            vms_type=obj_in.vms_type if obj_in.vms_type else to_update_vms.vms_type,
        )
        self.login_vms(login_info)
        return super().update(db_obj=to_update_vms, obj_in=obj_in)

    def remove_vms(self, *, id: str):
        return super().remove(id=id)

    def remove_my_company_vms(self, *, user: User):
        vms: VMS = self.get_my_company_vms(user=user)
        return self.remove_vms(id=str(vms.id))

    def check_status(self, response, verbose: bool):
        if response.status_code == requests.codes.ok:
            if verbose:
                print("Request successful\n{0}".format(response.text))
            return True
        print(
            response.url
            + " Request error {0}\n{1}".format(response.status_code, response.text)
        )
        return False

    def request_api(self, url, uri, method, **kwargs):
        server_url = f"{url}{uri}"
        response = requests.request(method, server_url, **kwargs)
        if not self.check_status(response, False):
            raise HTTPException(detail="Request error", status_code=500)
        if response.headers.get("Content-Type") == "application/json":
            return response.json()
        else:
            return response.content

    def login_vms(self, login_info: LoginInfo):
        if login_info.vms_type == VmsTypeEnum.nx:
            payload = {
                "username": login_info.username,
                "password": login_info.password,
                "setCookie": False,
            }
            uri = "/rest/v1/login/sessions"
        elif login_info.vms_type == VmsTypeEnum.oryza:
            payload = {
                "username": login_info.username,
                "password": login_info.password,
            }
            uri = "/api/v1/login"
        else:
            raise HTTPException(status_code=403, detail="Sai thông tin VMS.")

        url = login_info.ip_address + ":" + str(login_info.port)
        try:
            print("Login to VMS", url, payload)
            session = self.request_api(
                url,
                uri,
                "POST",
                verify=False,
                json=payload,
                timeout=5,
            )
        except Exception:
            raise HTTPException(status_code=403, detail="Sai thông tin VMS.")
        # Login failed
        if "error" in session:
            if session["errorString"]:
                if session["errorString"] == "Wrong password.":
                    raise HTTPException(status_code=401, detail="Sai mật khẩu.")
                raise HTTPException(status_code=401, detail=session["errorString"])
            raise HTTPException(status_code=401, detail="Unauthorized")
        if "token" not in session:
            return HTTPException(status_code=401, detail="Unauthorized")
        # Login success
        return session, url

    def get_auth_header(self, vms_info: VMS):
        session, url = self.login_vms(vms_info)
        # Login success
        token = session["token"]
        if vms_info.vms_type == VmsTypeEnum.nx:
            token_info = self.request_api(
                url, f"/rest/v1/login/sessions/{token}", "GET", verify=False, timeout=5
            )
            if token_info["expiresInS"] < 1:
                return HTTPException(status_code=401, detail="Token expired")
        return {"Authorization": f"Bearer {token}"}


vms_services = CRUDVMS(VMS)
