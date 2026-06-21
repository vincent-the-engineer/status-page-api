from server.utils.auth import (
    hash_api_key,
)


def test_hash_api_key():
    assert hash_api_key("test-key") == (
        "62af8704764faf8ea82fc61ce9c4c3908b6cb97d463a634e9e587d7c885db0ef"
    )
