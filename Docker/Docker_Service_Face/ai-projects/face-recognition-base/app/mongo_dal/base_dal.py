from mongoengine import Document
from datetime import datetime
from bson import ObjectId
from connect_db import connect_mongo_db

connect_mongo_db()


class BaseDAL:
    def __init__(self, model_class: Document):
        self.model_class = model_class
        collection_name = self.model_class._meta["collection"]
        self.collection = self.model_class._get_db()[collection_name]

    """---------------------MONGO ENGINE--------------------"""
    def save_document(self, list_data: list):
        # https://stackoverflow.com/questions/48028493/how-to-do-a-bulk-insert-with-mongoengine
        insert_list = [self.model_class(**data) for data in list_data]

        # bulk insert to MongoDB
        self.model_class.objects.insert(insert_list)

    def update_document(self, list_id: list, fields: list):
        """

        :param list_id:
        :param fields: list dictionary
        :return:
        """
        for i, mongo_id in enumerate(list_id):
            self.model_class.objects(id=mongo_id).update(**fields[i])

    def delete_document(self, list_id: list):
        for mongo_id in list_id:
            if isinstance(mongo_id, ObjectId):
                mongo_id = str(mongo_id)
            self.model_class.objects(id=mongo_id).delete()

    def drop_collection(self):
        self.collection.drop()

    # Function for query Using normal(find) or aggregation
    # https://docs.mongoengine.org/guide/querying.html#querying-the-database

    def find_all(self):
        return list(self.model_class.objects)

    def find_by_condition_field(self, field_condition: dict):
        # https://stackoverflow.com/questions/11876518/how-to-perform-such-filter-queries-in-mongoengine-on-nested-dicts-or-arrays-cont
        # https://docs.mongoengine.org/guide/querying.html#raw-queries
        return list(self.model_class.objects(__raw__=field_condition))

    """--------------------------PY MONGO Q Tai----------------------------------------------------------------"""
    def find_by_id(self, _id, columns=None):
        if isinstance(_id, str):
            _id = ObjectId(_id)

        return self.collection.find_one({"_id": _id}, projection=self.get_columns(columns))

    def find_one_by_condition(self, condition: dict, columns: dict = None):
        """

        :param condition: condition = {"job_id": data_example["job_id"]}
        :param columns: columns={"_id": 1}
        :return:
        """
        return self.collection.find_one(condition, projection=self.get_columns(columns))

    def find_object_id_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"_id": 1, "status_process": 1, "multiprocessing_pid": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data

    def create_one(self, data: dict, should_return_document=True):
        """

        :param data: data_example = {
                                        "job_id": user_id_grouping,
                                        "progress": 0,
                                        "created_at": datetime.now(),
                                    }
        :param should_return_document:
        :return:
        """
        if hasattr(self.model_class, "created_at"):
            data["created_at"] = datetime.now()

        self.model_class(**self.clone_ignore_id(data))
        item = self.collection.insert_one(data)

        if should_return_document:
            return self.find_by_id(item.inserted_id)

        return item.inserted_id

    def update(
        self,
        condition: dict,
        data: dict = None,
        set_on_insert: dict = None,
        push: dict = None,
        pull: dict = None,
        upsert=False,
    ):
        """

        :param condition: {"_id": mongo_id}
        :param data: {
                        "job_id": user_id_grouping,
                        "progress": 10,
                        "created_at": datetime.now(),
                    }
        :param set_on_insert:
        :param push:
        :param pull:
        :param upsert:
        :return:
        """
        update_data = {}

        if data is not None:
            self.model_class(**self.clone_ignore_id(data))
            update_data["$set"] = data
        if set_on_insert is not None:
            update_data["$setOnInsert"] = set_on_insert
        if push is not None:
            update_data["$push"] = push
        if pull is not None:
            update_data["$pull"] = pull

        result = self.collection.update_many(condition, update_data, upsert=upsert)

        return result.modified_count

    def delete(self, condition: dict):
        """

        :param condition: {"_id": mongo_id}
        :return:
        """
        result = self.collection.delete_many(condition)

        return result.deleted_count

    @staticmethod
    def get_columns(columns: dict = None):
        if columns:
            return columns

        return {"random_field": False}

    @staticmethod
    def clone_ignore_id(data):
        data_clone = data.copy()
        data_clone.pop("_id", None)

        return data_clone

    """--------------------------PY MONGO Q Tai---------------------------------------------------------------"""

    # Aggregation
    def aggregate(self, pipeline):
        try:
            return self.model_class.objects.aggregate(pipeline)
        except Exception as e:
            print(e)
            print("Error when connect to mongo DB")
            # while True:
            #     try:
            #         connect_mongo_db()
            #         from mongoengine import get_db
            #         db = get_db()
            #         db.command('ping')  # The 'ping' command is a simple way to test the connection
            #         print("Connected to MongoDB success")
            #         break
            #     except Exception as e:
            #         print(e)
            #         print("Loop to connect mongoDB")

            connect_mongo_db()
            return self.model_class.objects.aggregate(pipeline)

    def find_all_item(self):
        data = list(self.aggregate([]))
        return data

    def find_object_by_track_id_and_process_name(self, track_id, process_name):
        pipeline = [
            {"$match": {"track_id": track_id, "process_name": process_name}},
        ]
        data = list(self.aggregate(pipeline))
        return data

    def find_access_token_by_process_name(self, process_name):
        pipeline = [
            {"$match": {"process_name": process_name}},
            {"$project": {"access_token": 1}}
        ]
        data = list(self.aggregate(pipeline))
        return data