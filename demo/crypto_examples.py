import base64
import hashlib

from Crypto.Cipher import AES, DES


def md5_hash(data):
    """Calculate MD5 hash of input data"""
    md5_hasher = hashlib.md5()
    md5_hasher.update(data.encode())
    return md5_hasher.hexdigest()


def aes_encrypt(key, data):
    """Encrypt data using AES"""
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(data))


def des_encrypt(key, data):
    """Encrypt data using DES"""
    cipher = DES.new(key, DES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(data))


# Example usage
data = "Hello, World!"
key = b"SecretKey12345678"  # 16 bytes for AES
des_key = b"Secret78"  # 8 bytes for DES

print(f"MD5 Hash: {md5_hash(data)}")
print(f"AES Encrypted: {aes_encrypt(key, data)}")
print(f"DES Encrypted: {des_encrypt(des_key, data)}")
print(f"DES Encrypted: {des_encrypt(des_key, data)}")
