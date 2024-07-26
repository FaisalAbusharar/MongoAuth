from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class KeyManager:
    def __init__(self):
        # Load configuration from environment variables or config file
        try:
            from enviroment import MongoURI, MongoDatabase, MongoCollection, MongoKeyList
        except ImportError:
            MongoURI = os.getenv('MONGO_URI')
            MongoDatabase = os.getenv('MONGO_DATABASE')
            MongoCollection = os.getenv('MONGO_COLLECTION')
            MongoKeyList = os.getenv('MONGO_KEY_LIST')

        # Ensure MongoURI is correctly loaded
        if not MongoURI:
            raise ValueError("MongoURI is not set. Please check your environment variables or config file.")

        self.uri = MongoURI
        self.database_name = MongoDatabase
        self.collection_name = MongoCollection
        self.key_name_list = MongoKeyList

        # Initialize MongoDB client
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.database = self.client[self.database_name]

    def generate_sha256_hash(self, input_string):
        """Generate a SHA-256 hash for a given input string."""
        sha256 = hashlib.sha256()
        sha256.update(input_string.encode('utf-8'))
        return sha256.hexdigest()

    def connect_to_database(self):
        try:
            return self.database
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            exit()

    def generate_random_string(self, length=32):
        """Generate a random string of fixed length."""
        return os.urandom(length).hex()

    def initialize_keys_collection(self, amt: int, hash=None, key=None):
        db = self.connect_to_database()  # Connect to the database
        collection = db[self.collection_name]  # Connect to the collection
        document_list = []

        for _ in range(int(amt)):  # Generate keys equal to the amount entered by user
            random_string = self.generate_random_string()  # Generate the random string
            hashed = self.generate_sha256_hash(random_string) if hash is None else hash
            document_list.append({key: hashed})  # Append them to the list

        try:
            collection.insert_many(document_list)  # Insert them into the database
        except Exception as e:
            print(f"Error inserting documents: {e}")
            return None
        return collection

    def generate_auth(self, num, hash=None, keyListName=None):
        collection = self.initialize_keys_collection(amt=num, hash=hash, key=keyListName)
        return collection is not None  # Return True if the collection exists

    def generate_keys(self, outputM=True, hashM=None, amtM=None, keyNameListM=None):
        amount = amtM or int(input("Enter how many keys you'd like to generate: "))
        keyNameListFinal = keyNameListM or self.key_name_list

        if self.generate_auth(num=amount, hash=hashM, keyListName=keyNameListFinal):
            if outputM:
                print(f"Generated {amount} keys successfully.")
        else:
            if outputM:
                print("Failed to generate keys.")
            exit()

    def gen(self, hash='default', keyNameList='default', amt="ask", output=True):
        # Default values for hash, keyNameList, and amt
        hash = None if hash == 'default' else hash
        keyNameList = None if keyNameList == 'default' else keyNameList
        amt = None if amt == 'ask' else int(amt)

        # Call generate_keys with the parsed parameters
        self.generate_keys(outputM=output, hashM=hash, amtM=amt, keyNameListM=keyNameList)

# Example usage
if __name__ == "__main__":
    key_manager = KeyManager()
    key_manager.gen()
