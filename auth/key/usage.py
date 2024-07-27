from key_authenticator import KeyAuthenticator

def main():
    # Example 1: Basic usage with user input for the key
    print("Example 1: Basic usage with user input for the key")
    KeyAuthenticator.authKey(
        output=True,
        ask_for_key=True,
        key=None,
        key_list_name=None,
        auth_user_with_ip=True,
        auth_user_with_hostname=True,
        check_if_user_auth=True,
        user_ip=None,
        user_hostname=None
    )

    # Example 2: Using a provided key with IP and hostname authentication
    print("\nExample 2: Using a provided key with IP and hostname authentication")
    provided_key = "EXAMPLE-SERIAL-KEY-123"
    KeyAuthenticator.authKey(
        output=True,
        ask_for_key=False,
        key=provided_key,
        key_list_name=None,
        auth_user_with_ip=True,
        auth_user_with_hostname=True,
        check_if_user_auth=True,
        user_ip=None,
        user_hostname=None
    )

    # Example 3: Using only hostname for authentication
    print("\nExample 3: Using only hostname for authentication")
    KeyAuthenticator.authKey(
        output=True,
        ask_for_key=True,
        key=None,
        key_list_name=None,
        auth_user_with_ip=False,
        auth_user_with_hostname=True,
        check_if_user_auth=True,
        user_ip=None,
        user_hostname=None
    )

    # Example 4: Disabling both IP and hostname authentication
    print("\nExample 4: Disabling both IP and hostname authentication")
    KeyAuthenticator.authKey(
        output=True,
        ask_for_key=True,
        key=None,
        key_list_name=None,
        auth_user_with_ip=False,
        auth_user_with_hostname=False,
        check_if_user_auth=False,
        user_ip=None,
        user_hostname=None
    )

if __name__ == "__main__":
    main()
