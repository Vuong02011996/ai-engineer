# CAUTION: THIS IS NOT USED ANYMORE. THIS SCRIPT IS USED TO ADD PORT_RTSP TO CAMERA COLLECTION IN MONGODB.

# As camera is unique by (ip_address, port_rtsp), not (ip_address, port), we need to add a new field port_rtsp to the Camera model.

from pymongo import MongoClient


def get_port_rtsp(rtsp: str) -> int:
    """
    Get port from rtsp. Rtsp alway have port.
    For example: rtsp://192.168.111.6:80/ -> 80: int
    """
    return int(rtsp.split(":")[-1].split("/")[0])


def add_port_rtsp_camera(db_name: str, collection_name: str, client_uri: str):
    client = MongoClient(client_uri)
    db = client[db_name]
    collection = db[collection_name]

    docs = collection.find()

    for doc in docs:
        rtsp = doc["rtsp"]
        if rtsp == "":
            continue
        port_rtsp = get_port_rtsp(rtsp)
        collection.update_one({"_id": doc["_id"]}, {"$set": {"port_rtsp": port_rtsp}})
        print("Updated: ", doc["_id"])


if __name__ == "__main__":
    db_uri = "localhost:27018"
    db_name = "oryza-ai_db_test"
    collection_name = "camera"
    add_port_rtsp_camera(db_name, collection_name, db_uri)
