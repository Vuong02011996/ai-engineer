from fastapi import HTTPException
from odmantic import query

from app.core.config import settings
from app.services.base_services import CRUDBase
from app.models.brand_camera_model import BrandCamera
from app.schemas.brand_camera_schemas import BrandCameraCreate, BrandCameraUpdate


class CRUDBrandCamera(CRUDBase[BrandCamera, BrandCameraCreate, BrandCameraUpdate]):
    def count_brand_camera(self, data_search: str = None) -> int:
        # common_conditions = query.match(BrandCamera.key, {"$ne": "OTHER"})
        if data_search:
            search_conditions = BrandCamera.name.match(f".*{data_search}.*")
            combined_conditions = query.and_(
                # common_conditions,
                search_conditions,
            )
            return self.engine.count(BrandCamera, combined_conditions)
        return self.engine.count(
            BrandCamera,
            # common_conditions
        )

    def get_brand_camera(self, *, id: str):
        brand_camera = super().get(id)
        if not brand_camera:
            raise HTTPException(status_code=404, detail="Brand Camera not found")
        return brand_camera

    def get_by_key(self, *, key: str):
        return self.engine.find_one(BrandCamera, BrandCamera.key == key)

    def get_id_by_name(self, *, name: str):
        brand = self.engine.find_one(BrandCamera, BrandCamera.name == name)
        if brand:
            return str(brand.id)
        else:
            return None

    def get_by_name(self, *, name: str):
        return self.engine.find_one(BrandCamera, BrandCamera.name == name)

    def get_brand_cameras(
        self, *, page: int = 0, page_break: bool = False, data_search: str = None
    ):
        # common_conditions = query.match(BrandCamera.key, {"$ne": "OTHER"})

        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )

        if data_search:
            search_conditions = BrandCamera.name.match(f".*{data_search}.*")
            combined_conditions = query.and_(
                # common_conditions,
                search_conditions,
            )
            cursor = self.engine.find(
                BrandCamera,
                combined_conditions,
                **offset,
                sort=BrandCamera.created.desc(),
            )
        else:
            cursor = self.engine.find(
                BrandCamera,
                # common_conditions,
                **offset,
                sort=BrandCamera.created.desc(),
            )

        return list(cursor)

    def create_brand_camera(self, *, obj_in: BrandCameraCreate):
        if not isinstance(obj_in, dict):
            obj_in = obj_in.model_dump()
        brand_camera = self.engine.find_one(
            BrandCamera, BrandCamera.name == obj_in["name"]
        )
        if brand_camera:
            raise HTTPException(status_code=400, detail="Brand Camera already exists")
        brand_camera = self.engine.find_one(
            BrandCamera, BrandCamera.key == obj_in["key"]
        )
        if brand_camera:
            raise HTTPException(
                status_code=400, detail="Brand Camera key already exists"
            )
        return super().create(obj_in=obj_in)

    def update_brand_camera(self, *, id: str, obj_in: BrandCameraUpdate):
        brand_camera = self.get_brand_camera(id=id)
        if not brand_camera:
            raise HTTPException(status_code=404, detail="Brand Camera not found")

        name = obj_in.name
        exist_brand_camera = self.engine.find_one(
            BrandCamera, BrandCamera.name == name, BrandCamera.id != id
        )
        if exist_brand_camera:
            raise HTTPException(
                status_code=400, detail="Brand Camera name already used"
            )
        key = obj_in.key
        exist_brand_camera = self.engine.find_one(
            BrandCamera, BrandCamera.key == key, BrandCamera.id != id
        )
        if exist_brand_camera:
            raise HTTPException(status_code=400, detail="Brand Camera key already used")
        return super().update(db_obj=brand_camera, obj_in=obj_in)

    def delete_brand_camera(self, *, id: str):
        from app.services.camera_services import camera_services

        camera_services.remove_camera_brand(brand_id=id)
        return super().remove(id=id)


brand_camera_services = CRUDBrandCamera(BrandCamera)
