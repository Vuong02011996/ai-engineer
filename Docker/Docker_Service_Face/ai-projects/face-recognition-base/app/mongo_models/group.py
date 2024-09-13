from mongoengine import (
    Document,
    StringField,
    LongField,
    LazyReferenceField,
    DateTimeField,
    BooleanField

)
import datetime


class ProcessGroup(Document):
    job_id = StringField(required=True)
    progress = LongField(required=True)
    type = StringField(required=True)
    status = StringField(required=True)
    # has_img_undefined = StringField(required=True)
    has_img_undefined = BooleanField(default=None)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    meta = {"collection": "process_group"}