"""
Webdisplay Server
Device Manager Encryption Handler

License: MIT license

Author: C2311231

Notes:
"""

import json
import os

import argon2.low_level
import cryptography.hazmat.primitives.ciphers.aead
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

import logging

def derive_key(pairing_code: str, salt: bytes) -> bytes:
    return argon2.low_level.hash_secret_raw(
        secret=pairing_code.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,  # 64 MB
        parallelism=4,
        hash_len=32,
        type=argon2.low_level.Type.ID,
    )


def encrypt_pairing_data(pairing_code: str, data: dict) -> dict:
    """
    Encrypt pairing data using a key derived from the pairing code.
    """
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(pairing_code, salt)

    cipher = ChaCha20Poly1305(key)

    plaintext = json.dumps(data).encode()

    ciphertext = cipher.encrypt(
        nonce,
        plaintext,
        None
    )

    return {
        "salt": salt.hex(),
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex(),
    }


def encrypt_msg(key: bytes, data: bytes) -> tuple[bytes, bytes]:
    nonce: bytes = os.urandom(12)

    cipher: cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305 = cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305(key)
    ciphertext: bytes = cipher.encrypt(nonce, data, None)

    return nonce, ciphertext


def decrypt_msg(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes | None:
    cipher: cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305 = cryptography.hazmat.primitives.ciphers.aead.ChaCha20Poly1305(key)

    try:
        return cipher.decrypt(nonce, ciphertext, None)
    except ValueError:
        logging.error("Decryption failed. Invalid key or corrupted data.")
        return None
