from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from tools.enviroment import *
import random



load_dotenv()


uri = MongoURI # EDIT THIS URL IN THE .ENV FILE
client = MongoClient(uri, server_api=ServerApi('1'))

def connect_to_database():
    try:
        database = client[MongoDatabase]
        return database
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        exit()

def get_random_key():
    database = connect_to_database()
    collection = database[MongoCollection]

    #! Get the count of all documents in the collection
    count = collection.count_documents({})

    if count == 0:
        print("No serial keys found in the database.")
        return

    #! Generate a random index
    random_index = random.randint(0, count - 1)

    #! Retrieve the document at the random index
    random_key_document = collection.find().skip(random_index).limit(1)
    
    for document in random_key_document:
        print("Random Serial Key:", document[MongoKeyList])

if __name__ == "__main__":
    get_random_key()
