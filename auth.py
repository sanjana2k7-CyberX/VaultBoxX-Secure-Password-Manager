import hashlib

MASTER_PASSWORD = "mysecret123"

MASTER_HASH = hashlib.sha256(
    MASTER_PASSWORD.encode()
).hexdigest()

def verify_master_password(password):

    entered_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    return entered_hash == MASTER_HASH