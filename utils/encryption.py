from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_file_content(content, key=None):
    if not key:
        key = generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(content.encode())
    return encrypted

def decrypt_file_content(encrypted_content, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_content).decode()
    return decrypted
