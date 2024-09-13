from fastapi import HTTPException
from odmantic import ObjectId
from app.core.config import settings
from app.services.base_services import CRUDBase
from app.models import GeoUnit
from app.schemas import GeoUnitCreate, GeoUnitUpdate
from app.common.constants.enums import GeoUnitType


class CRUDGeoUnit(CRUDBase[GeoUnit, GeoUnitCreate, GeoUnitUpdate]):
    def get_units(
        self,
        page: int = 0,
        page_break: bool = False,
        type: GeoUnitType = None,
        parent_id: str = None,
        keyword: str = None,
    ):
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        query = {}
        if type:
            query["type"] = type
            if parent_id:
                if type == GeoUnitType.district:
                    query["province_id"] = parent_id
                elif type == GeoUnitType.ward:
                    query["district_id"] = parent_id
        if keyword:
            query["name"] = {"$regex": keyword, "$options": "i"}

        return self.engine.find(GeoUnit, query, **offset, sort=GeoUnit.created.asc())

    def count_geo_unit(
        self,
        type: GeoUnitType = None,
        parent_id: str = None,
        keyword: str = None,
    ):
        query = {}
        if type:
            print("type", type)
            query["type"] = type
            if parent_id:
                if type == GeoUnitType.district:
                    query["province_id"] = parent_id
                elif type == GeoUnitType.ward:
                    query["district_id"] = parent_id
        if keyword:
            query["name"] = {"$regex": keyword, "$options": "i"}
        return self.engine.count(GeoUnit, query)

    def get_list_ward_id(self, unit_id: str):
        geo_unit = self.get(id=unit_id)
        if not geo_unit:
            raise HTTPException(status_code=404, detail="Geo unit not found")
        if geo_unit.type == GeoUnitType.ward:
            return [unit_id]
        elif geo_unit.type == GeoUnitType.district:
            wards = self.engine.find(GeoUnit, GeoUnit.district_id == unit_id)
        elif geo_unit.type == GeoUnitType.province:
            wards = self.engine.find(GeoUnit, GeoUnit.province_id == unit_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid geo unit type")
        return [str(ward.id) for ward in list(wards)]

    def search_by_name(self, kw: str):
        rs = self.engine.find(GeoUnit, {"name": {"$regex": kw, "$options": "i"}})
        return list(rs)

    def create(self, *, obj_in: GeoUnitCreate):
        if obj_in.type == GeoUnitType.province:
            obj_in.district_id = None
            obj_in.ward_id = None

        elif obj_in.type == GeoUnitType.district:
            obj_in.ward_id = None
            if not obj_in.province_id:
                raise HTTPException(status_code=400, detail="Province ID is required")
            if not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.province_id)
            ):
                raise HTTPException(status_code=404, detail="Province not found")

        elif obj_in.type == GeoUnitType.ward:
            if not obj_in.district_id:
                raise HTTPException(status_code=400, detail="District ID is required")
            if not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.district_id)
            ):
                raise HTTPException(status_code=404, detail="District not found")
            if not obj_in.province_id:
                district = self.engine.find_one(
                    GeoUnit, GeoUnit.id == ObjectId(obj_in.district_id)
                )
                obj_in.province_id = district.province_id
            elif not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.province_id)
            ):
                raise HTTPException(status_code=404, detail="Province not found")
        return super().create(obj_in=obj_in)

    def update(self, *, id: str, obj_in: GeoUnitUpdate):
        if obj_in.type == GeoUnitType.province:
            obj_in.district_id = None
            obj_in.ward_id = None
            if not obj_in.province_id:
                raise HTTPException(
                    status_code=400, detail="Province ID is not required"
                )
            if not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.province_id)
            ):
                raise HTTPException(status_code=404, detail="Province not found")
        elif obj_in.type == GeoUnitType.district:
            obj_in.ward_id = None
            if not obj_in.province_id:
                raise HTTPException(status_code=400, detail="Province ID is required")
            if not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.province_id)
            ):
                raise HTTPException(status_code=404, detail="Province not found")
        elif obj_in.type == GeoUnitType.ward:
            if not obj_in.district_id:
                raise HTTPException(status_code=400, detail="District ID is required")
            if not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.district_id)
            ):
                raise HTTPException(status_code=404, detail="District not found")
            if not obj_in.province_id:
                district = self.engine.find_one(
                    GeoUnit, GeoUnit.id == ObjectId(obj_in.district_id)
                )
                obj_in.province_id = district.province_id
            elif not self.engine.find_one(
                GeoUnit, GeoUnit.id == ObjectId(obj_in.province_id)
            ):
                raise HTTPException(status_code=404, detail="Province not found")
        return super().update(id=id, obj_in=obj_in)

    def delete(self, *, id: str):
        unit = self.engine.find_one(GeoUnit, GeoUnit.id == id)
        if not unit:
            raise HTTPException(status_code=404, detail="Geo unit not found")
        if unit.type == GeoUnitType.province:
            district_count = self.engine.count(
                GeoUnit, GeoUnit.province_id == ObjectId(id)
            )
            if district_count > 0:
                raise HTTPException(
                    status_code=400, detail="Cannot delete province with districts"
                )
        elif unit.type == GeoUnitType.district:
            ward_count = self.engine.count(GeoUnit, GeoUnit.district_id == ObjectId(id))
            if ward_count > 0:
                raise HTTPException(
                    status_code=400, detail="Cannot delete district with wards"
                )
        return super().remove(id=id)

    def get_address_full(self, ward_id: str):
        try:
            wardId = ObjectId(ward_id)
        except Exception:
            return ""
        ward = self.engine.find_one(self.model, self.model.id == wardId)
        if not ward:
            return ""
        try:
            districtId = ObjectId(ward.district_id)
            provinceId = ObjectId(ward.province_id)
        except Exception:
            return ""
        district = self.engine.find_one(self.model, self.model.id == districtId)
        province = self.engine.find_one(self.model, self.model.id == provinceId)
        return f"{ward.name}<>{district.name}<>{province.name}"


geo_unit_services = CRUDGeoUnit(GeoUnit)

# for testing
if __name__ == "__main__":
    # Test search_by_name
    # print(geo_unit_services.search_by_name("An Giang"))

    # districts = geo_unit_services.get_districts_by_province(province_id="66cedf0163a3b21901eabcb3")
    # print(districts["total"])
    # for d in districts["data"]:
    #   print(d)

    wards = geo_unit_services.get_wards_by_district(
        district_id="66cedf0163a3b21901eabcb4"
    )
    print(wards["total"])
    for w in wards["data"]:
        print(w)
