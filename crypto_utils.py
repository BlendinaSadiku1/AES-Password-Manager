import base64
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PBKDF2_ITERATIONS = 200_000


def b64e(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')


def b64d(data: str) -> bytes:
    return base64.b64decode(data.encode('utf-8'))


def generate_salt() -> bytes:
    return os.urandom(16)


def hash_master_password(password: str, salt: bytes) -> str:
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32
    )
    return b64e(hashed)