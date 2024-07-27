from key_generator import KeyManager
from key_retriever import KeyRetriever

def main():
    # Example usage of KeyManager to generate keys
    print("=== Key Manager ===")
    key_manager = KeyManager()
    
    # Generating keys with default parameters
    print("Generating keys with default parameters...")
    key_manager.gen()

    # Generating keys with custom parameters
    print("\nGenerating keys with custom parameters...")
    key_manager.gen(hash="CUSTOM_HASH", key_name_list="CustomKeyList", amt=5)

    # Example usage of KeyRetriever to retrieve random keys
    print("\n=== Key Retriever ===")
    key_retriever = KeyRetriever()

    # Retrieving a single random key
    print("Retrieving a single random key...")
    key_retriever.retrieve_random_key(output=True)

    # Retrieving multiple random keys
    print("\nRetrieving multiple random keys...")
    key_retriever.retrieve_random_key(number_of_keys=3, output=True, key_list_name="CustomKeyList")

if __name__ == "__main__":
    main()

