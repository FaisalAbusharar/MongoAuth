from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
import os
import socket
import hashlib
import os
from dotenv import load_dotenv
from tools.enviroment import *

load_dotenv()


# MongoDB URI
uri = MongoURI # EDIT THIS URL IN THE .ENV FILE
client = MongoClient(uri, server_api=ServerApi('1'))

def generate_sha256_hash(input_string):
    """Generate a SHA-256 hash for a given input string."""
    sha256 = hashlib.sha256()
    sha256.update(input_string.encode('utf-8'))
    return sha256.hexdigest()


def connect_to_database():
    try:
        database = client[MongoDatabase]
        return database
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        exit()

def generate_random_string(length=32):
    """Generate a random string of fixed length."""
    return os.urandom(length).hex()

def initialize_keys_collection(amt):
    database = connect_to_database() #! Connect to database
    collection = database[MongoCollection] #! Connect to Collection
    document_list = []
    for i in range(amt): #* Generate keys equal to amount entered by user
        random_string = generate_random_string() #* Generate the random string
        sha256_hash = generate_sha256_hash(random_string) #! Create a sha256 Hash with the hash.
        document_list.append({MongoKeyList: sha256_hash}) #? Append them to the list
    collection.insert_many(document_list) #* Insert them to the database.
    return collection

def generate_auth(num):
    """I planned for the collection to return true if it worked, but this works too"""
    collection = initialize_keys_collection(num)
    if collection is not None: # this checks if the collection is valid/exists
        return True
    else:
        return False

def generateKey():
    amount = int(input("Enter how many keys you'd like to generate: "))
    if generate_auth(amount):
        print(f"Generated {amount} keys successfully.")
    else:
        print("Failed to generate keys.")
        input()
        exit()



generateKey()

