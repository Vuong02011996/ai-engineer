from enum import Enum
from datetime import datetime
from mongoengine import (
    StringField,
    DateTimeField,
    FloatField,
    IntField,
    BooleanField,
    LazyReferenceField,
    Document,
    LongField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    EnumField,
    URLField,
)


class ObjectAttendance(Document):
    process_name = StringField(required=True)
    track_id = IntField(required=True, min_value=0)
    avatars = StringField(required=True)
    avatars_ori = StringField(required=True)
    result_ai = StringField()
    from_frame = IntField(required=True, min_value=0)
    to_frame = IntField(min_value=0)
    acc_face = IntField(min_value=0)
    have_new_face = BooleanField(default=False, required=True)
    identity = LazyReferenceField("Identity")
    similarity_distance = FloatField()
    identity_name = StringField()
    avatars_match = StringField()
    created_at = DateTimeField(default=datetime.utcnow, required=True)

    meta = {"collection": "objects_attendance"}