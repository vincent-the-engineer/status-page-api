from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


_ph = PasswordHasher()

def hash_api_key(api_key: str) -> str:
    return _ph.hash(api_key)
