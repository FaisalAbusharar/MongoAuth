from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import random

class KeyRetriever:
    def __init__(self, uri=None, database=None, collection=None, key_list=None):
        # Load environment variables if not provided
        load_dotenv()
        self.uri = uri or os.getenv('MONGO_URI')
        self.database_name = database or os.getenv('MONGO_DATABASE')
        self.collection_name = collection or os.getenv('MONGO_COLLECTION')
        self.key_list = key_list or os.getenv('MONGO_KEY_LIST')

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
        for _ in range(number_of_keys):
            # Generate a random index
            random_index = random.randint(0, count - 1)

            # Retrieve the document at the random index
            random_key_document = collection.find().skip(random_index).limit(1)
            for document in random_key_document:
                random_keys.append(document.get(key_list_name))

        if output:
            if number_of_keys == 1:
                print("Random Serial Key:", random_keys[0])
            else:
                print("Random Serial Keys:", random_keys)

        return random_keys
