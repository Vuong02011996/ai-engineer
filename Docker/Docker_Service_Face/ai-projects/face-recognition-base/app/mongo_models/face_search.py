from enum import Enum
from mongoengine import (
    StringField,
    DateTimeField,
    Document,
    LongField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    EnumField,
    URLField,
    FloatField,
    IntField
)
import datetime


class IdentityType(Enum):
    HOCSINH = "Hoc Sinh"
    GIAOVIEN = "Giao Vien"
    NHANVIEN = "Nhan Vien"
    PHUHUYNH = "Phu Huynh"


class IdentityStatus(Enum):
    TRACKING = "tracking"
    UNTRACKING = "untracking"


class MatchingFace(EmbeddedDocument):
    face_id = LongField(required=True)
    url_face = StringField(required=True)
    url_ori = StringField(required=True)
    types = StringField(required=True)
    threshold = FloatField(required=True)
    width_img = IntField(required=True)
    height_img = IntField(required=True)
    accuracy_face_detect = FloatField(required=True)


class FaceSearch(Document):
    name = StringField(required=True)
    user_id = StringField(required=True)
    branch_id = StringField(required=True)
    branch_name = StringField(required=True)
    class_id = StringField(required=True)
    class_name = StringField(required=True)
    data = ListField(StringField(required=True))
    type = EnumField(IdentityType, default=IdentityType.HOCSINH, required=True)
    status = EnumField(IdentityStatus, default=IdentityStatus.TRACKING)
    matching_face_ids = ListField(EmbeddedDocumentField(MatchingFace))
    created_at = DateTimeField(default=datetime.datetime.utcnow, required=True)
    original_url = StringField()
    # meta = {"collection": "face_search"}
    meta = {
        "collection": None  # Placeholder, will be set dynamically
    }

    @classmethod
    def set_collection_name(cls, collection_name):
        cls._meta["collection"] = collection_name