from app.mongo_dal.base_dal import BaseDAL
from app.mongo_models.object_model.object_attendance import ObjectAttendance


class ObjectAttendanceDAL(BaseDAL):
    def __init__(self):
        super().__init__(ObjectAttendance)

    def find_object_id_by_track_id(self, track_id, process_name):
        pipeline = [
            {"$match": {"track_id": track_id, "process_name": process_name}},
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_object_id_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"_id": 1, "track_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_all_object_have_name_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"_id": 1, "track_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_object_have_face_id_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name, "have_new_face": True}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_object_by_name(self, name):
        pipeline = [
            {"$match": {"identity_name": name}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_object_by_identity(self, identity):
        pipeline = [
            {"$match": {"identity": identity}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_all_object_have_face(self):
        pipeline = [
            {"$match": {"have_new_face": True}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def delete_all_by_process_name(self, process_name):
        object_id = self.find_object_id_by_process_name(process_name)
        if len(object_id) > 0:
            list_id = list(map(lambda x: x["_id"], object_id))
            self.delete_document(list_id)


if __name__ == '__main__':
    object_dal = ObjectAttendanceDAL()
    object_dal.drop_collection()