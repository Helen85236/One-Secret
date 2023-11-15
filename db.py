import pymongo
import os

cluster = pymongo.MongoClient(os.getenv('MONGO_DB_URL'))
database = cluster["test"]["test"]
