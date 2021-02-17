import binascii
import os
from base64 import b64decode, b64encode
from typing import Optional

from content_size_limit_asgi import ContentSizeLimitMiddleware
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from api.config import HOST, MAX_CONTENT_SIZE, PORT

app = FastAPI()
app.add_middleware(ContentSizeLimitMiddleware, max_content_size=MAX_CONTENT_SIZE)


class CryptoData(BaseModel):
    data: str
    associated_data: Optional[str]


@app.post("/api/encrypt/", response_class=ORJSONResponse)
async def api_encrypt(body: CryptoData):
    data, associated_data = deserialize(body)
    ciphertext, key, nonce = encrypt(data, associated_data)
    return {
        "ciphertext": b64encode(ciphertext),
        "key": b64encode(key),
        "nonce": b64encode(nonce),
    }


def deserialize(body: CryptoData):
    try:
        data = b64decode(body.data)
    except (binascii.Error, TypeError):
        raise HTTPException(400, "data must be base64 string")
    try:
        if body.associated_data:
            associated_data = b64decode(body.associated_data)
        else:
            associated_data = None
    except (binascii.Error, TypeError):
        raise HTTPException(400, "associated-data must be base64 string")

    return data, associated_data


def encrypt(data: bytes, associated_data: bytes):
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, associated_data)
    return ciphertext, key, nonce


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
