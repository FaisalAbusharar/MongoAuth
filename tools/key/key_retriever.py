from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import random

class KeyRetriever:
    def __init__(self, uri=None, database=None, collection=None, key_list=None):
        # Load environment variables if not provided
        load_dotenv()
        try:
            from enviroment import MongoURI, MongoDatabase, MongoCollection, MongoKeyList
        except ImportError:
            MongoURI = os.getenv('MONGO_URI')
            MongoDatabase = os.getenv('MONGO_DATABASE')
            MongoCollection = os.getenv('MONGO_COLLECTION')
            MongoKeyList = os.getenv('MONGO_KEY_LIST')

        self.uri = MongoURI
        self.database_name = MongoDatabase
        self.collection_name = MongoCollection
        self.key_list = MongoKeyList

        # Ensure MongoURI is correctly loaded
        if not self.uri:
            raise ValueError("MongoURI is not set. Please check your environment variables or config file.")
        
        # Initialize MongoClient
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

    def connect_to_database(self):
        """ Connect to the MongoDB database. """
        try:
            return self.database
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            exit()

    def retrieve_random_key(self, number_of_keys=1, key_list_name=None, output=True):
        """ Retrieve a specified number of random keys from the MongoDB collection. """
        key_list_name = key_list_name or self.key_list
        db = self.connect_to_database()
        collection = db[self.collection_name]
        # Get the count of all documents in the collection
        count = collection.count_documents({})
        if count == 0:
            if output:
                print("No serial keys found in the database.")
            return []

        random_keys = []
        correctlyRetrivedAmount=number_of_keys
        for _ in range(number_of_keys):
            # Generate a random index
            random_index = random.randint(0, count - 1)

            # Retrieve the document at the random index
            random_key_document = collection.find().skip(random_index).limit(1)
            for document in random_key_document:
                if document is not None:
                    random_keys.append(document.get(key_list_name))
                    for i in random_keys:
                        if i==None and key_list_name != self.key_list:
                            correctlyRetrivedAmount -= 1
                            random_keys.remove(i)
                        else:
                            pass
        if correctlyRetrivedAmount < number_of_keys:
                    if output: print(f"Retrieved {number_of_keys- correctlyRetrivedAmount} improper keys, please do not mix a collection with multiple key list names.")
              
        if output:
            if number_of_keys == 1 and random_keys[0] != None:
                print("Random Serial Key:", random_keys[0])
            elif number_of_keys == 1 and random_keys[0] == None:
                print("Retrieved an improper key, please do not mix a collection with mutliple key list names")
            else:
                print("Random Serial Keys:", random_keys)

        return random_keys
