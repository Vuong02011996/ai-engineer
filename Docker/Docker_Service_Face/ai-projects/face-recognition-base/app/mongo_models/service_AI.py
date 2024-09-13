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


class ServiceAI(Document):
    name_service = StringField(required=True)
    port_service_head = IntField(required=True)
    port_service_face = IntField(required=True)
    ip_service = StringField(required=True)
    status_service = StringField(required=True)
    rtsp_cam_running = StringField(required=True)
    process_name = StringField(required=True)
    num_cam_running = IntField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)
    meta = {"collection": "services_ai"}