from enum import Enum
from mongoengine import (
    StringField,
    DateTimeField,
    Document,
    IntField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    EnumField,
    FloatField,
)
import datetime


class StatusCam(Enum):
        DISCONNECT = "DISCONNECT"
        CONNECT = "CONNECT"


class Coordinates(EmbeddedDocument):
    name_regions = StringField(required=True)
    coord = ListField(ListField(FloatField(min_value=0, required=True), required=True), required=True)


class RollCall(EmbeddedDocument):
    from_time = StringField(required=True)
    to_time = StringField(required=True)
    process_name = StringField(required=True)
    status_process = StringField(required=True)
    coordinates = ListField(ListField(FloatField(min_value=0, required=True), required=True), required=True)


class Sleepless(EmbeddedDocument):
    from_time = StringField(required=True)
    to_time = StringField(required=True)
    duration_time = IntField(required=True)
    process_name = StringField(required=True)
    status_process = StringField(required=True)
    coordinates = ListField(EmbeddedDocumentField(Coordinates))


class SafeAreaRegions(EmbeddedDocument):
    from_time = StringField(required=True)
    to_time = StringField(required=True)
    duration_time = IntField(required=True)
    process_name = StringField(required=True)
    status_process = StringField(required=True)
    coordinates = ListField(EmbeddedDocumentField(Coordinates))


class FallDetection(EmbeddedDocument):
    from_time = StringField(required=True)
    to_time = StringField(required=True)
    duration_time = IntField(required=True)
    process_name = StringField(required=True)
    status_process = StringField(required=True)
    coordinates = ListField(EmbeddedDocumentField(Coordinates))


class BehaviorGeneral(EmbeddedDocument):
    from_time = StringField(required=True)
    to_time = StringField(required=True)
    duration_time = StringField(required=True)
    coordinates = ListField(ListField(FloatField(min_value=0, required=True), required=True), required=True)


class Behavior(EmbeddedDocument):
    sleepless = EmbeddedDocumentField(BehaviorGeneral)
    play_alone = EmbeddedDocumentField(BehaviorGeneral)
    fall_down = EmbeddedDocumentField(BehaviorGeneral)
    fight = EmbeddedDocumentField(BehaviorGeneral)


class JobsCam(EmbeddedDocument):
    roll_call = EmbeddedDocumentField(RollCall)
    # sleepless = EmbeddedDocumentField(RollCall)
    sleepless = EmbeddedDocumentField(Sleepless)
    # safe_area_regions = ListField(EmbeddedDocumentField(SafeAreaRegions))
    safe_area_regions = EmbeddedDocumentField(SafeAreaRegions)
    fall_detection = EmbeddedDocumentField(FallDetection)


class Camera(Document):
    id_camera = StringField(required=True)
    username_cam = StringField(required=True)
    password_cam = StringField(required=True)
    url_cam = StringField(required=True)
    ip_host_socket = StringField(required=True)
    port_host_socket = StringField(required=True)
    address = StringField(required=True)
    #  Job cam
    jobs_cam = EmbeddedDocumentField(JobsCam, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)
    meta = {"collection": "cameras"}