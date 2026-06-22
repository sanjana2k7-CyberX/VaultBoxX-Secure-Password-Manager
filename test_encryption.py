from encryption import (
    encrypt_password,
    decrypt_password
)

master = "mysecret123"

encrypted = encrypt_password(
    "password123",
    master
)

print("Encrypted:")
print(encrypted)

decrypted = decrypt_password(
    encrypted,
    master
)

print("Decrypted:")
print(decrypted)