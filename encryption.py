from cryptography.fernet import Fernet
import hashlib
import base64

def generate_key(master_password):
    key = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_password(password, master_password):
    key = generate_key(master_password)
    cipher = Fernet(key)

    return cipher.encrypt(
        password.encode()
    ).decode()

def decrypt_password(encrypted_password, master_password):
    key = generate_key(master_password)
    cipher = Fernet(key)

    return cipher.decrypt(
        encrypted_password.encode()
    ).decode()