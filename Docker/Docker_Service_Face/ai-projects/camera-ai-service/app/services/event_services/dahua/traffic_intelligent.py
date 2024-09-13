import logging
import os
from io import BytesIO
import time
import json

from app.core.config import settings
from app.services.minio_services import minio_services
from app.services.event_services.dahua.dahua_base import DahuaBase
from app.common.enum import VehicleBrand, Color

logger = logging.getLogger("TI")


class TrafficIntelligent(DahuaBase):
    def __init__(self, config: dict):
        import random

        super().__init__(config)
        # Setting from request
        self.name = f"Traffic Intelligent Camera {random.randint(1, 1000)}"
        self.code = "[All]"
        self.rbmq_exchange = "PLATE_NUMBER_EXCHANGES"
        self.construct_url()

    def custom_decode(self, content: dict):
        # Timestamp

        timestamp = int(content.get("UTC", 0))
        if timestamp == 0:
            return {}
        timestamp = timestamp - 7 * 3600  # Convert to UTC+0

        # TODO: 4 lines below For testing purpose, Remove when go production
        # event_code = content.get("Code")
        # with open(f"temp/{timestamp}_{event_code}.txt", "w") as file:
        #     print(f"Got content {event_code}")
        #     file.write(json.dumps(content, indent=4))

        comm_info: dict = content.get("CommInfo", {})
        vehicle_category = comm_info.get("SnapCategory", "")
        # print(
        #     f"Vehicle category: {vehicle_category}"
        # )  # TODO: For monitoring, Remove this line
        if vehicle_category == "NonMotor":
            data = self.decode_non_motor(content)
        else:
            data = self.decode_motor(content)
        # print(f"Data: {data}") # TODO: For monitoring, Remove this line
        data["timestamp"] = timestamp
        data = {
            **data,
            "is_wrong_lane": False,
            "video": "",
            "weight": "",  # width, not weight
            "is_over_load": False,
            "weight_overload": "",
            "is_oversize": False,
            "volume_oversize": "",
            "vehicle_length": "",
            "vehicle_height": "",
            "vehicle_width": "",
            "front_img": "",
            "back_img": "",
            "location_id": "",
        }
        if "violation" in data:
            violation_code: str = data["violation"]
            if violation_code == ("Cross Solid White Line"):
                data["event_traffic"].append("TRAFFIC_OVERLINE")
            elif violation_code == "Wrong-way Driving":
                data["event_traffic"].append("TRAFFIC_RETROGRADE")
            elif violation_code == "Cross Solid Yellow Line":
                data["event_traffic"].append("TRAFFIC_OVERYELLOWLINE")
            elif violation_code == "Illegal Lane Change":
                data["event_traffic"].append("TRAFFIC_CROSSLANE")
            elif (
                violation_code == "Unfasten Seat Belt"
                and "TRAFFIC_NOSEATBELT" not in data["event_traffic"]
            ):
                data["event_traffic"].append()
            elif (
                violation_code == "Calling While Driving"
                and "TRAFFIC_CALLING" not in data["event_traffic"]
            ):
                data["event_traffic"].append("TRAFFIC_CALLING")
            elif (
                violation_code == "Smoking While Driving"
                and "TRAFFIC_SMOKING" not in data["event_traffic"]
            ):
                data["event_traffic"].append("TRAFFIC_SMOKING")
            elif violation_code == "Non-motor Vehicle in Lane":
                data["event_traffic"].append("TRAFFIC_WRONGROUTE")
            elif (
                violation_code == "No Helmet"
                and "TRAFFIC_NOHELMET" not in data["event_traffic"]
            ):
                data["event_traffic"].append("TRAFFIC_NOHELMET")

        logger.info(f"\nCustom decode: {data}\n")
        return data

    def decode_non_motor(self, content: dict):
        lane = content.get("Lane", "")

        non_motor: dict = content.get("NonMotor", {})
        plate: dict = content.get("Plate", {})
        if plate == {}:
            plate: dict = non_motor.get("Plate", {})
        if plate != {}:
            plate_number = plate.get("Text", "Không xác định")
            if plate_number != "Không xác định" and not self.validate_plate(
                plate_number
            ):
                plate_number = f"Xác định sai: {plate_number}"
            plate_bounding_box = plate.get("BoundingBox", [0, 0, 0, 0])
        else:
            plate_number = ""
            plate_bounding_box = [0, 0, 0, 0]
        speed = non_motor.get("Speed", 0)
        vehicle_type = non_motor.get("Category", "")
        vehicle_color = non_motor.get("Color", "")
        rider_list: list[dict] = content.get("RiderList", [{}])
        main_rider: dict = rider_list[0]
        helmet = [self.evaluate_condition(main_rider.get("Helmet", None), "1", [])]
        if len(rider_list) > 1:
            sub_rider: dict = rider_list[1]
            helmet.append(
                self.evaluate_condition(sub_rider.get("Helmet", None), "1", [])
            )
        traffic_car: dict = content.get("TrafficCar", {})
        if traffic_car != {}:
            violation = traffic_car.get("ViolationName", "")
            violation_code = traffic_car.get("ViolationCode", "")
            plate_color = traffic_car.get("PlateColor", "")
            if vehicle_color == "":
                vehicle_color = traffic_car.get("VehicleColor", "")
            # TODO: 1 line below for collecting data purposes, remove when go production
            # bounding_box = traffic_car.get("BoundingBox", [0, 0, 0, 0])

        # our traffic code
        event_traffic = []
        if helmet[0] == "no" or (len(helmet) > 1 and helmet[1] == "no"):
            event_traffic.append("TRAFFIC_NOHELMET")

        return {
            # TODO: line below for collecting data purposes, remove when go production
            # "vehicle_bbox": bounding_box if bounding_box else "",
            "lane": lane if lane else "",
            "license_plate": plate_number if plate_number else "",
            "plate_color": plate_color,
            "vehicle_type": vehicle_type if vehicle_type else "Không xác định",
            "speed": speed if speed else 0,
            "license_plate_bounding_boxes": plate_bounding_box
            if plate_bounding_box
            else [0, 0, 0, 0],
            "brand_name": "Không xác định",
            "helmet": helmet if helmet else "",
            "violation": violation if violation else "",
            "violation_code": violation_code if violation_code else "",
            "vehicle_color": vehicle_color,
            "event_traffic": event_traffic if event_traffic else [],
        }

    def decode_motor(self, content: dict):
        traffic_car: dict = content.get("TrafficCar", {})
        if traffic_car != {}:
            plate_number = traffic_car.get("PlateNumber", "")
            if plate_number == "":
                return {}
            if not self.validate_plate(plate_number):
                plate_number = f"Xác định sai: {plate_number}"
            plate_color = traffic_car.get("PlateColor", "")
            brand_name: str = traffic_car.get("VehicleSign")
            brand_name = (
                VehicleBrand.unknown
                if brand_name.lower() == "unknown"
                else brand_name.upper()
            )
            vehicle_color = traffic_car.get("VehicleColor", Color.unknown)
            violation = traffic_car.get("ViolationName", "")
            violation_code = traffic_car.get("ViolationCode", "")

            # TODO: 2 lines below for collecting data purposes, remove when go production
        #     bounding_box = traffic_car.get("BoundingBox", [0, 0, 0, 0])
        lane = content.get("Lane", "")

        vehicle: dict = content.get("Vehicle", {})
        if vehicle != {}:
            plate: dict = vehicle.get("Plate", {})
            if plate != {}:
                plate_bounding_box = plate.get("BoundingBox", [0, 0, 0, 0])

        # if not found bounding box, try again with the "object"
        obj: dict = content.get("Object", {})
        if obj != {} and obj.get("ObjectType") == "Plate":
            plate_bounding_box = obj.get("BoundingBox", [0, 0, 0, 0])

        speed = content.get("Speed", 0)
        common_info: dict = content.get("CommInfo", {})
        vehicle_type = common_info.get("StandardVehicleType", "Không xác định")
        main_seat: dict = vehicle.get("MainSeat", {})
        sub_seat: dict = vehicle.get("SubSeat", {})

        calling = [
            self.evaluate_condition(
                main_seat.get("DriverCalling"), "Calling", ["NotCalling"]
            ),
            self.evaluate_condition(
                sub_seat.get("DriverCalling"), "Calling", ["NotCalling"]
            ),
        ]
        safe_belt = [
            self.evaluate_condition(
                main_seat.get("SafeBelt"), "WithSafeBelt", ["WithoutSafeBelt"]
            ),
            self.evaluate_condition(
                sub_seat.get("SafeBelt"), "WithSafeBelt", ["WithoutSafeBelt"]
            ),
        ]
        smoking = [
            self.evaluate_condition(
                main_seat.get("DriverSmoking"), "Smoking", ["NotSmoking"]
            ),
            self.evaluate_condition(
                sub_seat.get("DriverSmoking"), "Smoking", ["NotSmoking"]
            ),
        ]

        # our traffic code
        event_traffic = []
        if safe_belt[0] == "no" or safe_belt[1] == "no":
            event_traffic.append("TRAFFIC_NOSEATBELT")
        if smoking[0] == "yes" or smoking[1] == "yes":
            event_traffic.append("TRAFFIC_SMOKING")
        if calling[0] == "yes":
            event_traffic.append("TRAFFIC_CALLING")

        return {
            # TODO: 1 lines below for collecting data purposes, comment out when go production
            # "vehicle_bbox": bounding_box if bounding_box else "",
            "lane": lane if lane else "",
            "license_plate": plate_number if plate_number else "",
            "plate_color": plate_color,
            "vehicle_type": vehicle_type if vehicle_type else "Ô tô",
            "speed": speed if speed else 0,
            "license_plate_bounding_boxes": plate_bounding_box
            if plate_bounding_box
            else [0, 0, 0, 0],
            "brand_name": brand_name if brand_name else "Không xác định",
            "calling": calling if calling else "",
            "safe_belt": safe_belt if safe_belt else "",
            "smoking": smoking if smoking else "",
            "violation": violation if violation else "",
            "violation_code": violation_code if violation_code else "",
            "vehicle_color": vehicle_color,
            "event_traffic": event_traffic if event_traffic else [],
        }

    def evaluate_condition(self, condition, positive_value, negative_values):
        from app.common.enum import TrafficIntelligentStatusEnum as EStatus

        if condition == positive_value:
            return EStatus.yes
        elif condition in negative_values:
            return EStatus.no
        else:
            return EStatus.na

    def validate_plate(self, plate: str):
        import re

        pattern = re.compile(r"(^\d{2}[A-Z]{2}\d{4,5}$)|(^\d{2}[A-Z]\d{4,6}$)")
        match = pattern.search(plate)
        return match

    def custom_data_to_send(self, data: dict, image):
        if "license_plate" not in data or data["license_plate"] == "":
            logger.info("No license plate found")
            return {}
        event_time = data.get("event_time", int(time.time()))
        filename = f"dh_ti_{event_time}"

        # TODO: For collecting data purposes, remove when go production. After this, image and text will be saved
        ###############################################
        # if self.address == "14.241.88.21":
        #     temp_folder = "14"
        # elif self.address == "tieuhocbinhmy2.quickddns.com":
        #     temp_folder = "binhmy"
        # else:
        #     temp_folder = "unknown"
        # temp_folder = f"collect_ti_{temp_folder}"
        # if not os.path.exists(f"./temp/{temp_folder}"):
        #     os.makedirs(f"./temp/{temp_folder}")
        # filename = f"{temp_folder}/{filename}"
        # with open(
        #     f"./temp/{filename}_{random.randint(1, 1000)}{random.choice(string.ascii_letters)}.json",
        #     "wb",
        # ) as file:
        #     file.write(json.dumps(data, indent=4).encode("utf-8"))
        ###############################################

        # Save the image content to a file
        big_image_name, full_img_path = super().save_temp_image(
            image, temp_name=filename
        )

        data = self.map_vehicle_info(data)
        data = {
            **data,
            "full_img": minio_services.upload_file(
                full_img_path, big_image_name, bucket=settings.BUCKET_PLATE
            ),
            "crop_plate": self.crop_plate(
                full_img_path, data["license_plate_bounding_boxes"]
            )
            if data.get("license_plate_bounding_boxes") != [0, 0, 0, 0]
            else "",
            "camera_ip": self.address,
        }

        # TODO: For collecting data purposes, UNCOMMENT below lines when go production
        try:
            os.remove(full_img_path)
        except Exception:
            pass

        logger.info(f"\nCustom data: {data}\n")
        return data

    def map_vehicle_info(self, data: dict):
        try:
            with open("app/common/vehicle_mapping.json", "r") as file:
                mapping: dict = json.load(file)
                vehicle_type_mapping: dict = mapping.get("vehicle_type", "")
                vehicle_color_mapping: dict = mapping.get("vehicle_color", "")
                violation_mapping: dict = mapping.get("violation", "")

                # TODO: For collecting data purposes, remove when go production
                ###############################################################
                # if vehicle_type_mapping.get(data["vehicle_type"], "") == "":
                #     with open("temp/new_vehicle_type.txt", "a") as file:
                #         file.write(f"{data['vehicle_type']}\n")
                # if vehicle_color_mapping.get(data["vehicle_color"], "") == "":
                #     with open("temp/new_vehicle_color.txt", "a") as file:
                #         file.write(f"{data['vehicle_color']}\n")
                # if violation_mapping.get(data["violation"], "") == "":
                #     with open("temp/new_violation.txt", "a") as file:
                #         file.write(f"{data['violation']}\n")
                ###############################################################

                data["vehicle_type"] = vehicle_type_mapping.get(
                    data["vehicle_type"], data["vehicle_type"]
                )  # If not found, return the original value
                data["vehicle_color"] = vehicle_color_mapping.get(
                    data["vehicle_color"], data["vehicle_color"]
                )  # If not found, return the original value
                data["plate_color"] = vehicle_color_mapping.get(
                    data["plate_color"], data["plate_color"]
                )
                data["violation"] = violation_mapping.get(
                    data["violation"], data["violation"]
                )  # If not found, return the original value

        except Exception as e:
            print(f"Error reading mapping file: {e}")
        return data

    def crop_plate(self, image_path, bbox: list):
        from PIL import Image

        # Open the image
        if bbox == [0, 0, 0, 0]:
            return False
        image = Image.open(image_path)
        # First crop the infor bar on the top
        width, height = image.size
        left_top_remap = (int(bbox[0]) / 8192, int(bbox[1]) / 8192)
        right_bottom_remap = (int(bbox[2]) / 8192, int(bbox[3]) / 8192)
        left_top_remap = (
            int(left_top_remap[0] * width),
            int(left_top_remap[1] * height),
        )
        right_bottom_remap = (
            int(right_bottom_remap[0] * width),
            int(right_bottom_remap[1] * height),
        )

        # The crop rectangle, as a (left, upper, right, lower)-tuple.
        crop_rectangle = (
            left_top_remap[0] * 0.98,
            left_top_remap[1] * 0.98,
            right_bottom_remap[0] * 1.04,
            right_bottom_remap[1] * 1.06,
        )
        # Perform the crop
        cropped_image = image.crop(crop_rectangle)
        # Convert the cropped image to bytes
        img_byte_arr = BytesIO()
        try:
            cropped_image.save(img_byte_arr, format="JPEG")
        except Exception:
            return False
        img_byte_arr = img_byte_arr.getvalue()
        # Save or display the cropped image
        crop_name = f"crop_plate_ti_{int(time.time())}"
        temp_image_name, temp_image_path = super().save_temp_image(
            img_byte_arr, crop_name
        )
        if temp_image_path and temp_image_name:
            crop_url = minio_services.upload_file(
                temp_image_path, temp_image_name, bucket=settings.BUCKET_PLATE
            )
            os.remove(temp_image_path)
            return crop_url


if __name__ == "__main__":
    import re

    test_values = [
        "61K09823",
        "34A63247",
        "18AB1234",
        "18AB12345",
        "18A12345",
        "18A123456",
        "18A1234",
        "18AB123",
        "18AB123456",
    ]

    pattern = re.compile(r"(^\d{2}[A-Z]{2}\d{4,5}$)|(^\d{2}[A-Z]\d{5,6}$)")
    for value in test_values:
        if pattern.match(value):
            print(f"{value} matches")
        else:
            print(f"{value} does not match")
