import pymongo
import os

cluster = pymongo.MongoClient(os.getenv('MONGO_DB_URL'))
database = cluster[os.getenv('db_name')]["kv"]
