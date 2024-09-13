import json
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate
from app.schemas.company_schemas import CompanyCreate
from app.schemas.camera_schemas import CameraCreate
from app.services import company_services, user_services, camera_services
from pymongo.database import Database
from app.core.config import settings
from app.db.session import MongoDatabase


def init_db(db: Database) -> None:
    # Create Oryza company if not exists
    company_in = CompanyCreate(name="Oryza", domain="oryza.vn")
    company = company_services.create(obj_in=company_in)  # noqa: F841

    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL,
        username=settings.FIRST_SUPERUSER_USERNAME,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        company_id=str(company.id),
        is_superuser=True,
        is_active=True,
    )
    superuser: User = user_services.get_by_email(email=user_in.email)
    if superuser:
        user_services.remove(id=superuser.id)
    superuser = user_services.create_user(obj_in=user_in, is_active=True)
    # Create normal user
    user_in = UserCreate(
        email=settings.FIRST_USER_EMAIL,
        username=settings.FIRST_USER_USERNAME,
        password=settings.FIRST_USER_PASSWORD,
        company_id=str(company.id),
        is_superuser=False,
        is_active=True,
    )
    normal_user: User = user_services.get_by_email(email=user_in.email)
    if normal_user:
        user_services.remove(id=normal_user.id)
    normal_user = user_services.create_user(obj_in=user_in, is_active=True)

    dahua_bt = {
        "name": "OryzaRDBT",
        "ip_address": "192.168.111.6",
        "port": 80,
        "username": "admin",
        "password": "Oryza@123",
        "rtsp": "rtsp://",
    }
    camera2_in = {
        "name": "Ross, Cohen and Manning",
        "ip_address": "192.168.111.7",
        "port": 80,
        "username": "edwardsmichelle",
        "password": "(co#%3ExBp",
        "rtsp": "http://cuevas-scott.info/tags/app/categoryregister.html",
    }
    camera_in = CameraCreate(**dahua_bt)
    camera = camera_services.create_camera(user=normal_user, obj_in=camera_in)
    camera2 = camera_services.create_camera(user=normal_user, obj_in=camera2_in)

    # Save user and company
    company = company.model_dump()
    company = {
        "id": str(company["id"]),
        "name": company["name"],
        "domain": company["domain"],
    }
    superuser = superuser.model_dump()
    superuser = {
        "id": str(superuser["id"]),
        "email": superuser["email"],
        "username": superuser["username"],
        "is_superuser": superuser["is_superuser"],
        "is_active": superuser["is_active"],
    }
    normal_user = normal_user.model_dump()
    normal_user = {
        "id": str(normal_user["id"]),
        "email": normal_user["email"],
        "username": normal_user["username"],
        "is_superuser": normal_user["is_superuser"],
        "is_active": normal_user["is_active"],
    }
    camera = camera.model_dump()
    dahua_bt_camera = {
        "id": str(camera["id"]),
        "name": camera["name"],
        "ip_address": camera["ip_address"],
        "port": camera["port"],
        "username": camera["username"],
        "password": camera["password"],
        "rtsp": camera["rtsp"],
        "company": str(camera["company"]["id"]),
    }
    camera2 = camera2.model_dump()
    camera2 = {
        "id": str(camera2["id"]),
        "name": camera2["name"],
        "ip_address": camera2["ip_address"],
        "port": camera2["port"],
        "username": camera2["username"],
        "password": camera2["password"],
        "rtsp": camera2["rtsp"],
        "company": str(camera2["company"]["id"]),
    }
    save_data = {
        "company": company,
        "superuser": superuser,
        "normal_user": normal_user,
        "camera": dahua_bt_camera,
        "camera2": camera2,
    }
    print(save_data)
    try:
        with open("./app/tests/init_db.json", "w") as f:
            json.dump(save_data, f, indent=4)
        print("Init DB done")
    except Exception as e:
        print(e)
        print("Init DB failed")


def read_initial_data():
    with open("app/tests/init_db.json") as f:
        data = json.load(f)
    return data


init_data = read_initial_data()


if __name__ == "__main__":
    db = MongoDatabase()
    init_db(db)

# TODO: Add more init data
