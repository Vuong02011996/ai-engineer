from app.schemas import (
    TypeServiceCreate,
    BrandCameraCreate,
)
from app.services import (
    type_service_services,
    brand_camera_services,
)
from app.common.constants.rabbitmq_constants import TypeServiceKey, type_service_name
from app.common.constants.type_camera import TypeCameraEnum


def create_type_services():
    for _key in TypeServiceKey:
        if _key.name in type_service_name:
            type_service_in = TypeServiceCreate(
                name=type_service_name[_key.name], key=_key.value
            )
            existed_type_service = type_service_services.get_by_key(key=_key.value)
            if not existed_type_service:
                type_service_services.create(obj_in=type_service_in)
                print(f"\nCreate type service {type_service_in.name}")
            else:
                type_service_services.update(
                    obj_in=type_service_in, db_obj=existed_type_service
                )
                print(f"\nUpdate type service {type_service_in.name}")

    existed_type_service = type_service_services.get_by_key(key="OTHER")
    if not existed_type_service:
        type_service_in = TypeServiceCreate(name="Khác", key="OTHER")
        type_service_services.create(obj_in=type_service_in)
        print(f"\nCreate type service {type_service_in.name}")
    else:
        type_service_services.update(
            obj_in={"name": "Khác"}, db_obj=existed_type_service
        )
        print("\nUpdate type service OTHER")


def create_brand_camera():
    brand_camera_in = BrandCameraCreate(name="Hãng khác", key="OTHER")
    existed_brand_camera = brand_camera_services.get_by_key(key="OTHER")
    if not existed_brand_camera:
        brand_camera_services.create(obj_in=brand_camera_in)
        print(f"\nCreate brand camera {brand_camera_in.name}")
    else:
        brand_camera_services.update(
            obj_in=brand_camera_in, db_obj=existed_brand_camera
        )
        print(f"\nUpdate brand camera {brand_camera_in.name}")

    for _key in TypeCameraEnum:
        brand_camera_in = BrandCameraCreate(
            name=_key.name.replace("_", " ").title(), key=_key.value
        )
        brand_camera_existed = brand_camera_services.get_by_key(key=_key.value)
        if not brand_camera_existed:
            brand_camera_services.create(obj_in=brand_camera_in)
            print(f"\nCreate brand camera {brand_camera_in.name}")
        else:
            brand_camera_services.update(
                obj_in=brand_camera_in, db_obj=brand_camera_existed
            )
            print(f"\nUpdate brand camera {brand_camera_in.name}")


if __name__ == "__main__":
    create_type_services()
    create_brand_camera()
