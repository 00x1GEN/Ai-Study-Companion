from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hash_roundtrip():
    hashed = hash_password("password123")
    assert verify_password("password123", hashed)
    assert not verify_password("wrong-password", hashed)

def test_access_token_roundtrip():
    token = create_access_token(42)
    assert decode_access_token(token) == 42
