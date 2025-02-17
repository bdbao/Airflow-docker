from pymongo import MongoClient
from urllib.parse import quote_plus
from module_connect.config_conn import settings

def connect_mongodb():
    mongo_url = settings.MONGO_URL_CONNECT.format(
        user=settings.MONGO_USER,
        password=quote_plus(settings.MONGO_PASSWORD),
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        database=settings.MONGO_DATABASE
    )
    client = MongoClient(mongo_url)
    db = client[settings.MONGO_DATABASE]
    return db

def mongodb_engine():
    # Return the formatted connection URL (useful for certain cases where URI is needed directly)
    return settings.MONGO_URL_CONNECT.format(
        user=settings.MONGO_USER,
        password=quote_plus(settings.MONGO_PASSWORD),
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        database=settings.MONGO_DATABASE
    )
