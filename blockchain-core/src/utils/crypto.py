# src/utils/crypto.py

import hashlib
import os
import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def generate_keypair():
    """Generate a new RSA key pair."""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def sign_message(message, private_key):
    """Sign a message with the given private key."""
    key = RSA.import_key(private_key)
    message_hash = SHA256.new(message.encode())
    signature = pkcs1_15.new(key).sign(message_hash)
    return binascii.hexlify(signature).decode()


def verify_signature(message, signature, public_key):
    """Verify a message signature with the given public key."""
    key = RSA.import_key(public_key)
    message_hash = SHA256.new(message.encode())
    try:
        pkcs1_15.new(key).verify(message_hash, binascii.unhexlify(signature))
        return True
    except (ValueError, TypeError):
        return False


def hash_data(data):
    """Return the SHA-256 hash of the given data."""
    return hashlib.sha256(data.encode()).hexdigest()
