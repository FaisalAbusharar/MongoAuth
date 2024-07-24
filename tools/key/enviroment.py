import os
from dotenv import load_dotenv

load_dotenv()

MongoURI = os.getenv('MONGO_CLIENT_SECRET_URL')
MongoDatabase = os.getenv('MONGO_DATABASE_NAME')
MongoCollection = os.getenv('MONGO_DATABASE_COLLECTION')
MongoKeyList = os.getenv('MONGO_COLLECTION_KEY_LIST')


def retrieveEnv():
    print(MongoURI, MongoCollection, MongoDatabase, MongoKeyList)