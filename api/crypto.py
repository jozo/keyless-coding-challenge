import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(data: bytes, associated_data: bytes):
    key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, associated_data)
    return ciphertext, key, nonce
