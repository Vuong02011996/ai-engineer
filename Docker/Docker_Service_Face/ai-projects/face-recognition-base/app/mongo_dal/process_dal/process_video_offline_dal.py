from app.mongo_dal.base_dal import BaseDAL
from app.mongo_models.process_model.process_video_offline import ProcessVideoOffline


class ProcessVideoOfflineDAL(BaseDAL):
    def __init__(self):
        super().__init__(ProcessVideoOffline)

    def find_object_id_by_camera_id(self, camera_id):
        pipeline = [
            {"$match": {"camera": camera_id}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_data_process_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"_id": 1, "fps_cam": 1, "url_cam": 1, }}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_camera_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"camera": 1, "job_process": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_process_id_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"process_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data


if __name__ == '__main__':
    process_dal = ProcessVideoOfflineDAL()
    process_dal.drop_collection()