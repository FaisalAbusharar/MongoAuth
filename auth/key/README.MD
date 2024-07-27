# Key Authentication 
This system provides the necessary files to implement key authentication into your projects.

## Uses
If you'd like to implement a serial key system into your projects, or lock certain things behind a needed key and have the security of a Mongo Database.

## Usage
You will only need the `key_authenticator.py` and optionally the `enviroment.py`, of course you can create a .env and use that instead, it'll work automatically with the project (*as long as it's in the same directory*).
You can also take a look at `usage.py` for usage examples.
The function you will mainly use is `authkey()`, here is a full example usage:
```python
 KeyAuthenticator.authKey(
        output=True, ask_for_key=True,
        key=None, key_list_name=None,
        auth_user_with_ip=True, auth_user_with_hostname=True,
        check_if_user_auth=True,
        user_ip=None, user_hostname=None
    )
```
It's HEAVILY recommended to provide an IP and/or Hostname, if it's not provided, it will grab the local IP and Hostname which may cause issues, you can provide these variables with the `user_ip` and `user_hostname` arguments.
You will receieve warnings based on the settings you choose, of course these can be disabled with `output=false`
Users can be authenticated/stored into the database with either IPs, Hostnames, or both.
You can disable the IP or Hostname authentication with `auth_user_with_ip` or `auth_user_with_hostname`.
A serial key can be provided with the `key` argument, this will not ask the user for a key even if `ask_for_key` is enabled.
You can skip checking if the user is already authenticated with the `check_if_user_auth=False` argument.
The `key_list_name` argument changes the name of the list that the program will look through, like `program-serial-key: {key}`.

# Warnings
You will recieve warnings, here is what each one means:

`[MONGOAUTH: WARNING] Users will not be authenticated because both IP auth and hostname auth are set to False.`
This means the user will not be authenticated since both IP and hostname authentication methods are set to false, `auth_user_with_ip=False` and `auth_user_with_hostname=False`

`[MONGOAUTH: WARNING] User will not be checked if already authenticated`
This means that the user will not be checked if they're already authenticated, `check_if_user_auth=False`

`[MONGOAUTH: WARNING] Mongoauth will acquire local hostname and user_ip since none are provided; this may provide unwanted results`
This is if both `user_ip` and `user_hostname` are empty, this will then acquire the local variables, which may cause errors.

`[MONGOAUTH: WARNING] Ask for key is enabled, however will not be used since key is not empty`
This occurs when `ask_for_key=True` and the `key` argument is not empty, this will ignore the `ask_for_key=True`.

`[MONGOAUTH: FAIL] No key was provided and 'ask_for_key' is false, therefore no key is given`
This occurs when `ask_for_key=False` and `key=None`, so this won't have any serial key to check, this is a fail and causes the function to return False.

All of these warnings (*except failures*) can be ignored with `output=False`.

