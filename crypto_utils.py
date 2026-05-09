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


def verify_master_password(password: str, salt: bytes, expected_hash_b64: str) -> bool:
    calculated = hash_master_password(password, salt)
    return calculated == expected_hash_b64


def derive_aes_key(master_password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode('utf-8'),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32
    )

def encrypt_text(plain_text: str, key: bytes) -> tuple[str, str]:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    cipher_text = aesgcm.encrypt(nonce, plain_text.encode('utf-8'), None)
    return b64e(nonce), b64e(cipher_text)


def decrypt_text(nonce_b64: str, cipher_text_b64: str, key: bytes) -> str:
    aesgcm = AESGCM(key)
    plain_text = aesgcm.decrypt(b64d(nonce_b64), b64d(cipher_text_b64), None)
    return plain_text.decode('utf-8')