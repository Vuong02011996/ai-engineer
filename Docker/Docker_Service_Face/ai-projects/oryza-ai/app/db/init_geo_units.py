import json
import os
from app.services import geo_unit_services
from app.schemas import GeoUnitCreate
from app.common.constants.enums import GeoUnitType

src = "app/db/geo_units.json"


def add_geo_units():
    if not os.path.exists(src):
        print("Geo units file not found")
        return
    with open(src, "r") as file:
        data = json.load(file)
        provinces = data["provinces"]
        for province in provinces:
            print(province["name"])
            obj_in = GeoUnitCreate(name=province["name"], type=GeoUnitType.province)
            new_province = geo_unit_services.create(obj_in=obj_in)

            # Add districts
            for district in province["districts"]:
                print(district["name"])
                obj_in = GeoUnitCreate(
                    name=district["name"],
                    type=GeoUnitType.district,
                    province_id=str(new_province.id),
                )
                new_district = geo_unit_services.create(obj_in=obj_in)

                # Add wards
                for ward in district["wards"]:
                    obj_in = GeoUnitCreate(
                        name=ward["name"],
                        type=GeoUnitType.ward,
                        district_id=str(new_district.id),
                    )
                    geo_unit_services.create(obj_in=obj_in)


if __name__ == "__main__":
    add_geo_units()
