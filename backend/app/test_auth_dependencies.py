import importlib
import os

import pytest
from jose import jwt


def test_security_exports_expected_jwt_contract():
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    security = importlib.import_module("app.auth.security")

    assert hasattr(security, "SECRET_KEY")
    assert hasattr(security, "ALGORITHM")
    assert security.ALGORITHM == "HS256"
    assert security.SECRET_KEY == "test-secret-key"


def test_create_access_token_uses_expected_contract():
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    security = importlib.import_module("app.auth.security")

    token = security.create_access_token("abc-123")
    payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])

    assert payload["sub"] == "abc-123"


def test_hash_password_rejects_passwords_over_72_bytes():
    os.environ["JWT_SECRET_KEY"] = "test-secret-key"
    security = importlib.import_module("app.auth.security")

    with pytest.raises(ValueError, match="72 bytes"):
        security.hash_password("a" * 73)
