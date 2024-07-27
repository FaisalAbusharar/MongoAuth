import socket
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

class KeyAuthenticator:
    def __init__(self) -> None:
        try:
            from enviroment import MongoURI, MongoDatabase, MongoCollection, MongoKeyList, MongoAuthCollection
        except ImportError:
            MongoURI = os.getenv('MONGO_URI')
            MongoDatabase = os.getenv('MONGO_DATABASE')
            MongoCollection = os.getenv('MONGO_COLLECTION')
            MongoKeyList = os.getenv('MONGO_KEY_LIST')
            MongoAuthCollection = os.getenv('MONGO_AUTH_COLLECTION')

        if not MongoURI:
            raise ValueError("MongoURI is not set. Please check your environment variables or config file.")

        self.uri = MongoURI
        self.database_name = MongoDatabase
        self.collection_name = MongoCollection
        self.key_name_list = MongoKeyList
        self.auth_collection_name = MongoAuthCollection

        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.database = self.client[self.database_name]
    
    def get_ip_address(self, mode=None):
        url = 'https://api.ipify.org'
        response = requests.get(url)
        ip_address = response.text
        hostname = socket.gethostname()
        if mode == "ip":
            return ip_address
        return hostname, ip_address

    def connect_to_database(self):
        try:
            return self.database
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            exit()

    def initialize_keys_collection(self):
        return self.database[self.collection_name]

    def return_collection(self, serial, key_list_name=None,
                           hostname=None, ip=None,
                           auth_with_ip=True, auth_with_hostname=True):
        collection = self.initialize_keys_collection()
        allowed_hosts = self.database[self.auth_collection_name]

        collection.delete_one({key_list_name or self.key_name_list: serial})
        
        USER_NAME = hostname or (socket.gethostname() if auth_with_hostname else None)
        IP = ip or (self.get_ip_address("ip") if auth_with_ip else None)

        if USER_NAME and IP:
            allowed_hosts.insert_one({"_id": USER_NAME, "ip_addr": IP})
        elif USER_NAME:
            allowed_hosts.insert_one({"_id": USER_NAME})
        elif IP:
            allowed_hosts.insert_one({"ip_addr": IP})

    def is_host_allowed(self, ip=None, hostname=None):
        allowed_hosts = self.database[self.auth_collection_name]
        if hostname == None: USER_NAME = socket.gethostname()
        else: USER_NAME = hostname
        if ip == None: IP = self.get_ip_address("ip")
        else: IP = ip

        check = allowed_hosts.find_one({"_id": USER_NAME, "ip_addr": IP})
        if check != None: return check
        check = allowed_hosts.find_one({"_id": USER_NAME})
        if check != None: return check
        check = allowed_hosts.find_one({"ip_addr": IP})
        if check != None: return check

    def license(self, check_if_user_auth=True, key_list_name=None,
                 ask_for_key=True, key=None,
                 auth_with_ip=True, auth_with_hostname=True,
                 ip=None, hostname=None):
        if check_if_user_auth and self.is_host_allowed(ip=ip, hostname=hostname):
            return True
        
        if ask_for_key != True and not key:
            print("[MONGOAUTH: FAIL] No key was provided and 'ask_for_key' is false, therefore no key is given")
            return False

        if ask_for_key == True and key != None: serial = key
        elif ask_for_key == True:
            serial = key or input("Serial key: ")
        collection = self.initialize_keys_collection()

        if key != None:
            serial = key

        if key_list_name:
            self.key_name_list = key_list_name

        if collection.find_one({self.key_name_list: serial}):
            self.return_collection(serial=serial, key_list_name=key_list_name,
                                   hostname=hostname, ip=ip,
                                   auth_with_ip=auth_with_ip,
                                   auth_with_hostname=auth_with_hostname)
            return True
        return False

    def authKey(output=True, ask_for_key=True, key=None, key_list_name=None, auth_user_with_ip=True, auth_user_with_hostname=True, check_if_user_auth=True, user_ip=None, user_hostname=None):
        key_manager = KeyAuthenticator()
        noAuth = False

        if output:
            if not auth_user_with_ip and not auth_user_with_hostname:
                print("[MONGOAUTH: WARNING] Users will not be authenticated because both IP auth and hostname auth are set to False.")
                noAuth = True
            elif not check_if_user_auth:
                print("[MONGOAUTH: WARNING] User will not be checked if already authenticated")
            elif not user_ip and not user_hostname and noAuth:
                print("[MONGOAUTH: WARNING] Mongoauth will acquire local hostname and user_ip since none are provided; this may provide unwanted results")
            elif ask_for_key == True and key != None:
                print("[MONGOAUTH: WARNING] Ask for key is enabled, however will not be used since key is not empty")
        if not key and not ask_for_key:
            print("[MONGOAUTH: FAIL] No key was provided and 'ask_for_key' is false, therefore no key is given")
            return False

        if output:
            if key_manager.license(check_if_user_auth, key_list_name, ask_for_key, key, auth_with_ip=auth_user_with_ip, auth_with_hostname=auth_user_with_hostname, ip=user_ip, hostname=user_hostname):
                print("[MONGOAUTH: SUCCESS] Serial key is valid")
                return True
            else:
                print("[MONGOAUTH: FAIL] Serial key provided is not valid")
                return False
        else:
            return key_manager.license(check_if_user_auth, key_list_name, ask_for_key, key, auth_with_ip=auth_user_with_ip, auth_with_hostname=auth_user_with_hostname, ip=user_ip, hostname=user_hostname)

if __name__ == "__main__":
    key_manager = KeyAuthenticator()
    # Example usage, if needed
    key_manager.authKey(key=None, user_ip="0.0.0", user_hostname="Host")
