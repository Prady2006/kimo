from pymongo import MongoClient
from  config.app_settings import app_settings

client = MongoClient(app_settings.mongo_host,app_settings.mongo_port)
db = client[app_settings.mongodb_name]
