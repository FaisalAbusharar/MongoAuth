import socket
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tools.enviroment import *


#@# -----------------------------------Database Functions----------------------------------- #@#

#! Connect to the database. This must be private.
uri = MongoURI
client = MongoClient(uri, server_api=ServerApi('1'))
#* Initialize The Client

def get_ip_address(mode=None):
    url = 'https://api.ipify.org'
    response = requests.get(url)
    ip_address = response.text
    hostname = socket.gethostname()
    if mode == "ip": #* Changes on what mode is selected, if mode isn't IP then both hostname and ip will be returned.
        return ip_address
    return hostname, ip_address #! return these so they can be stored in the database.

def connect_to_database(): #! Attempt to connect to the database.
    try:
        database = client["Auth"]
        return database
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        exit()

def initialize_keys_collection(): #* Connect to the collection where the keys are stored.
    database = connect_to_database()
    collection = database["keys"]
    return collection

def return_collection(serial):
    database = connect_to_database()
    collection = database["keys"]
    allowed_hosts = database["allowed-hosts"] #* Connect to the collection where the allowed hosts are stored.
    
    collection.delete_one({"program-serial-keys": serial}) #! Deletes the key after it gets used.
    
    USER_NAME = socket.gethostname()
    IP = get_ip_address("ip") 
    allowed_hosts.insert_one({"_id": USER_NAME, "ip_addr": IP}) #* Inserts the allowed users based on IP and Hostname

def is_host_allowed():
    database = connect_to_database()
    allowed_hosts = database["allowed-hosts"]
    
    USER_NAME = socket.gethostname()
    IP = get_ip_address("ip")
    return allowed_hosts.find_one({"_id": USER_NAME, "ip_addr": IP}) is not None #* This checks if the user exists in the allowed hosts area.

def license():
    if is_host_allowed(): 
        return True
    else:
        serial = input("Serial key: ")
        collection = initialize_keys_collection()
        
        if collection.find_one({"program-serial-keys": serial}):
            return_collection(serial)
            return True
        return False

def is_licensed():
    if license():
        os.system('cls' if os.name == 'nt' else 'clear')
        return True
    else:
        print("Please purchase a valid serial key.")
        input()
        exit()

#@# -----------------------------------LICENSE----------------------------------- #@#


def is_valid_key(): #key auth area.
    if is_licensed() == True:
        return True
    else:
        return False
