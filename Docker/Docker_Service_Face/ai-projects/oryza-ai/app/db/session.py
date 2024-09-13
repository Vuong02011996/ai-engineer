from app.core.config import settings
from pymongo import MongoClient
from odmantic import SyncEngine
import logging

logging.basicConfig(level=logging.INFO)


class _MongoClientSingleton:
    mongo_client: MongoClient
    engine: SyncEngine

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            uri = settings.MONGO_DATABASE_URI
            cls.instance.mongo_client = MongoClient(uri)
            database = settings.MONGO_DATABASE
            cls.instance.engine = SyncEngine(
                client=cls.instance.mongo_client, database=database
            )
            logging.info(f"Connected to database: {database}")
            logging.info(f"URI: {uri}")
        return cls.instance


def MongoDatabase():
    return _MongoClientSingleton().mongo_client[settings.MONGO_DATABASE]


def get_engine() -> SyncEngine:
    return _MongoClientSingleton().engine


async def ping():
    await MongoDatabase().command("ping")


__all__ = ["MongoDatabase", "ping"]
