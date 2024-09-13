from mongoengine import connect
from milvus import Milvus
from minio import Minio
import os
from dotenv import load_dotenv
import sys
import socket


debug = False
if debug:
    load_dotenv()
else:
    from pathlib import Path  # Python 3.6+ only

    if len(sys.argv) > 1:
        print("The script run with file {}".format(sys.argv[1]))
        env_path = Path(".") / sys.argv[1]
        print("env_path", env_path)
        load_dotenv(dotenv_path=env_path)
        print("Running in PORT: ", os.getenv("SERVER_PORT"))
    else:
        print("The script run with file .env")
        # env_path = Path(".") / ".env"
        # load_dotenv(dotenv_path=env_path)
        load_dotenv()


def connect_mongo_db():
    while True:
        try:
            connect(
                db=os.getenv("MONGO_DB_NAME"),
                host=os.getenv("MONGO_HOST"),
                port=int(os.getenv("MONGO_PORT")),
                username=os.getenv("MONGO_USERNAME"),
                password=os.getenv("MONGO_PASSWORD"),
                authentication_source="admin"
            )
            from mongoengine import get_db
            db = get_db()
            db.command('ping')  # The 'ping' command is a simple way to test the connection
            print("Connected to MongoDB success")
            print("MONGO_HOST: ", os.getenv("MONGO_HOST"))
            break
        except Exception as e:
            print(e)
            print("Loop to connect mongoDB")


def connect_milvus():
    milvus_client = Milvus(os.getenv("MILVUS_HOST"), int(os.getenv("MILVUS_PORT")))
    collection_name = os.getenv("collection_name")
    partition_name = os.getenv("partition_name")
    return milvus_client, collection_name, partition_name


def connect_minio():
    host = os.getenv("MINIO_HOST").split("//")[1]
    host = "{}:{}".format(host, os.getenv("MINIO_PORT"))
    bucket_name = os.getenv("MINIO_BUCKET")

    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")
    is_secure = os.getenv("MINIO_HOST").split(":")[0] == "https"

    minio_client = Minio(host, access_key=access_key, secret_key=secret_key, secure=is_secure)

    host_domain = "https://minio.core.greenlabs.ai"
    # host = ("https://" if is_secure else "http://") + host
    return minio_client, bucket_name, host_domain

def connect_socket():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((os.getenv("SOCKET_HOST"), int(os.getenv("SOCKET_PORT"))))

    return client_socket


if __name__ == '__main__':
    """
    MongoDB: docker-compose https://github.com/Vuong02011996/mongo_db/blob/master/docker-compose.yml
    MilvusDB: https://github.com/Vuong02011996/ai-engineer/blob/master/Database/Milvus/Milvus_0_10_6/install.sh
             http://localhost:3033/#/data/collections/clover_staging
    Minio: https://github.com/Vuong02011996/ai-engineer/blob/master/Database/Minio/docker-compose.yml
            https://minio.core.greenlabs.ai/minio/clover-staging/
    API: https://konga.core.greenlabs.ai/#!/upstreams (Vuong | 02011996)        
    """