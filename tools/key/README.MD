# Key Management System

This project provides a key management system using MongoDB for generating and retrieving serial keys. It includes two main classes:

* KeyGenerator: Generates and stores SHA-256 hashed keys in a MongoDB collection.
* KeyRetriever: Retrieves random keys from a MongoDB collection.

## Features

* Key Generation:
- * Generates a specified number of random keys.
- * Hashes keys using SHA-256.
-  * Stores generated keys in a MongoDB collection.
* Key Retrieval:
- * Retrieves a specified number of random keys from a MongoDB collection.
- * Supports key retrieval by specifying the key list name.
- * Provides output options for displaying the retrieved keys.
## Usage

### 1. Key Generation
File: `key_generator.py`

The `KeyGenerator` class handles generating and storing keys. Use the following example to generate keys:

```
python
from key_generator import KeyGenerator

# Initialize KeyGenerator with MongoDB configuration
key_gen = KeyGenerator(uri='YOUR_MONGO_URI', database='YOUR_DATABASE', collection='YOUR_COLLECTION', key_list='YOUR_KEY_LIST')

# Generate keys
key_gen.generate_keys(amount=10, hash=None, key_list_name='MyKeyList')
```

Parameters:

amount: Number of keys to generate.
hash: Optional SHA-256 hash to use (if not provided, a new hash will be generated).
key_list_name: Name of the key list to store the keys.
2. Key Retrieval
File: key_retriever.py

The KeyRetriever class retrieves random keys from the MongoDB collection. Use the following example to retrieve keys:

python
Copy code
from key_retriever import KeyRetriever

# Initialize KeyRetriever with MongoDB configuration
key_retriever = KeyRetriever(uri='YOUR_MONGO_URI', database='YOUR_DATABASE', collection='YOUR_COLLECTION', key_list='YOUR_KEY_LIST')

# Retrieve random keys
keys = key_retriever.retrieve_random_key(number_of_keys=5, key_list_name='MyKeyList', output=True)
Parameters:

number_of_keys: Number of random keys to retrieve.
key_list_name: Name of the key list to retrieve keys from.
output: Boolean flag to print the retrieved keys.
Configuration

Ensure you set up your environment variables or provide them directly in the code:

MONGO_URI: MongoDB connection URI.
MONGO_DATABASE: Name of the MongoDB database.
MONGO_COLLECTION: Name of the MongoDB collection.
MONGO_KEY_LIST: Name of the key list field in the collection.
Why and When to Use

When to Use:
Use KeyGenerator to create and store unique serial keys for applications, products, or services.
Use KeyRetriever to fetch random keys for validation, testing, or assignment purposes.
Why Use This System:
Provides a scalable and secure way to manage and store keys.
Easy integration with MongoDB for persistent storage and retrieval.