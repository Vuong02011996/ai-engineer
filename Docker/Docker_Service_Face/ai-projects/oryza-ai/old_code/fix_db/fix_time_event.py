from pymongo import MongoClient
from datetime import datetime


def remove_comma(db_name, collection_name):
    client = MongoClient(
        "mongodb://admin:1@192.168.105.212:27017,192.168.105.210:27017,192.168.105.225:27017/?authSource=admin&replicaSet=rs"
    )
    db = client[db_name]
    collection = db[collection_name]

    docs = collection.find()

    for doc in docs:
        if "timestamp" in doc["data"]:
            timestamp = str(doc["data"]["timestamp"])
            if "." in timestamp:
                timestamp = timestamp.split(".")[0]
                collection.update_one(
                    {"_id": doc["_id"]}, {"$set": {"data.timestamp": timestamp}}
                )
                print("Updated: ", doc["_id"])


def convert_timestamp(db_name, collection_name):
    client = MongoClient(
        "mongodb://admin:1@192.168.105.212:27017,192.168.105.210:27017,192.168.105.225:27017/?authSource=admin&replicaSet=rs"
    )
    db = client[db_name]
    collection = db[collection_name]

    docs = collection.find()

    # fix bug timestamp 30-5-2024
    # date = datetime.strptime('2024-05-30T05:13:03.000+00:00', '%Y-%m-%dT%H:%M:%S.%f%z')
    # docs = collection.find(
    #     { 'created': { '$gt': date } }
    # )

    for doc in docs:
        if "timestamp" in doc["data"] and doc["data"]["timestamp"] is not None:
            timestamp = str(doc["data"]["timestamp"])
            if len(timestamp) == 10:  # timestamp in seconds
                continue
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except Exception:
                timestamp = datetime.strptime(timestamp, "%d-%m-%Y %H:%M:%S")
            timestamp = str(int(timestamp.timestamp()))
            print(
                "Updated: ",
                doc["_id"],
                "old time:",
                doc["data"]["timestamp"],
                "new time:",
                timestamp,
            )
            collection.update_one(
                {"_id": doc["_id"]}, {"$set": {"data.timestamp": timestamp}}
            )


if __name__ == "__main__":
    db_name = "oryza-ai_db_test"  # change to "oryza-ai_db" when run in production
    collection_name = "event"
    # remove_comma(db_name, collection_name)
    convert_timestamp(db_name, collection_name)
