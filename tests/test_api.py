from base64 import b64encode

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.config import MAX_CONTENT_SIZE
from api.main import EncryptionData, app, deserialize

client = TestClient(app)


class TestApi:
    def test_returns_encrypted_data(self):
        response = client.post(
            "/api/encrypt/",
            json={
                "data": b64encode(b"hello").decode(),
                "associated_data": b64encode(b"world").decode(),
            },
        )

        data = response.json()

        assert response.status_code == 200
        assert "key" in data
        assert "nonce" in data
        assert "ciphertext" in data

    def test_associated_data_is_optional(self):
        response = client.post(
            "/api/encrypt/",
            json={
                "data": b64encode(b"hello").decode(),
            },
        )

        assert response.status_code == 200

    def test_content_size_is_limited(self):
        response = client.post(
            "/api/encrypt/",
            json={
                "data": b64encode(b"a" * 2 * MAX_CONTENT_SIZE).decode(),
            },
        )

        assert response.status_code == 400


class TestDeserialization:
    def test_ok_data(self):
        body = EncryptionData(data="aGVsbG8=", associated_data="d29ybGQ=")

        data, associated_data = deserialize(body)

        assert data == b"hello"
        assert associated_data == b"world"

    def test_data_must_contain_base64(self):
        with pytest.raises(HTTPException):
            body = EncryptionData(data="hello", associated_data="d29ybGQ=")
            deserialize(body)

    def test_associated_data_must_contain_base64(self):
        with pytest.raises(HTTPException):
            body = EncryptionData(data="aGVsbG8=", associated_data="world")
            deserialize(body)

    def test_associated_data_is_optional(self):
        body = EncryptionData(data="aGVsbG8=", associated_data=None)

        data, associated_data = deserialize(body)

        assert data == b"hello"
        assert associated_data is None
