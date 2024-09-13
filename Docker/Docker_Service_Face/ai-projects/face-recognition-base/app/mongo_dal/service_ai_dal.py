from app.mongo_dal.base_dal import BaseDAL
from app.mongo_models.service_AI import ServiceAI


class ServiceAIDAL(BaseDAL):
    def __init__(self):
        super().__init__(ServiceAI)

    def find_id_by_branch_id(self, branch_id):
        pipeline = [
            {"$match": {"branch_id": branch_id}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_id_by_id_camera(self, id_camera):
        pipeline = [
            {"$match": {"id_camera": id_camera}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_all_by_condition_field(self, field, condition):
        pipeline = [
            {"$match": {field: condition}},
            # {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_service_ai_id_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"_id": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

if __name__ == '__main__':
    camera_dal = ServiceAIDAL()
    camera_dal.drop_collection()