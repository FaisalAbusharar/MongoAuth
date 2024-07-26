import os
from dotenv import load_dotenv

load_dotenv('../')

MongoURI = os.getenv('MONGO_CLIENT_SECRET_URL') #This is the URI to connect to your database, mongoDB should give you this link.
MongoDatabase = os.getenv('MONGO_DATABASE_NAME') #The name of the Cluster/Database with the collections you want to access
MongoCollection = os.getenv('MONGO_DATABASE_COLLECTION') #The collection where the keys will be stored
MongoAuthCollection = os.getenv('MONGO_DATABASE_AUTH_COLLECTION') #The collection where authenticated users are stored.
MongoKeyList = os.getenv('MONGO_COLLECTION_KEY_LIST') #The name of the Keys, such as {'serial-key': xxxx}, serial-key is the name, can be anything.



def retrieveEnv():
    print(MongoURI, MongoCollection, MongoDatabase, MongoKeyList, MongoAuthCollection)

retrieveEnv()
