import binascii
from base64 import b64decode, b64encode
from typing import Optional

import structlog
from content_size_limit_asgi import ContentSizeLimitMiddleware
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from api.config import HOST, MAX_CONTENT_SIZE, PORT
from api.crypto import encrypt

log = structlog.get_logger()
app = FastAPI()
app.add_middleware(ContentSizeLimitMiddleware, max_content_size=MAX_CONTENT_SIZE)


class EncryptionData(BaseModel):
    data: str
    associated_data: Optional[str]


@app.get("/api/health/", response_class=ORJSONResponse)
async def api_health():
    return {"health": "ok"}


@app.post("/api/encrypt/", response_class=ORJSONResponse)
async def api_encrypt(body: EncryptionData, request: Request):
    """Encrypts provided data with AES-GCM. Data must be encoded in base64."""
    log.msg("Encryption call", client=f"{request.client.host}:{request.client.port}")
    data, associated_data = deserialize(body)
    ciphertext, key, nonce = encrypt(data, associated_data)
    return {
        "ciphertext": b64encode(ciphertext),
        "key": b64encode(key),
        "nonce": b64encode(nonce),
    }


def deserialize(body: EncryptionData):
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
