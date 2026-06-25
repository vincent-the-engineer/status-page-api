from server.db.schema.tables.user import (
    User,
)
from server.utils.auth import (
    hash_api_key,
    verify_api_key,
)


def test_hash_and_verify_api_key():
    api_key = "test-key"
    hash = hash_api_key(api_key)
    assert hash.startswith("$argon2")
    assert api_key not in hash
    assert verify_api_key(api_key, hash) is True
    wrong_api_key = "test-key2"
    assert verify_api_key(wrong_api_key, hash) is False
