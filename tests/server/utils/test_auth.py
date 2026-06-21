from server.db.schema.tables.user import SHA256_HASH_LENGTH
from server.utils.auth import (
    hash_api_key,
)


def test_hash_api_key():
    hash = hash_api_key("test-key")
    assert hash == (
        "62af8704764faf8ea82fc61ce9c4c3908b6cb97d463a634e9e587d7c885db0ef"
    )
    assert len(hash) == SHA256_HASH_LENGTH
