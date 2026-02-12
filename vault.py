import base64
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

VAULT_FILE = 'vault.enc'

def derive_key(master_password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations=100_000,
        backend=default_backend()
        )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def saveVault(vault, masterKey):
    salt = os.urandom(16)
    key = derive_key(masterKey, salt)
    cipher = Fernet(key)

    vault_bytes = json.dumps(vault).encode()
    encrypted_vault = cipher.encrypt(vault_bytes)

    with open(VAULT_FILE, 'wb') as f:
        f.write(salt + encrypted_vault)

def loadVault(masterKey):
    if not os.path.exists(VAULT_FILE):
        return {}
    
    with open(VAULT_FILE, 'rb') as f:
        data = f.read()

    salt = data[:16]
    encrypted_vault = data[16:]

    key = derive_key(masterKey, salt)
    cipher = Fernet(key)

    try:
        decrypted_bytes = cipher.decrypt(encrypted_vault)
        return json.loads(decrypted_bytes)
    except:
        return None




