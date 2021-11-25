from cryptography.fernet import Fernet
from pathlib import Path


class Encryption:
    key = None
    key_file_name = ".key"

    def __init__(self):
        if self.key_exists():
            self.load_key()
        else:
            self.generate_key()
            self.save_key()
        self.fernet = Fernet(self.key)

    def encrypt_string(self, string):
        return self.fernet.encrypt(string.encode()).decode()

    def decrypt_string(self, string):
        return self.fernet.decrypt(string.encode()).decode()

    def generate_key(self):
        self.key = Fernet.generate_key()

    def save_key(self):
        key_file = open(self.key_file_name, "wb")
        key_file.write(self.key)
        key_file.close()

    def load_key(self):
        key_file = open(self.key_file_name, "rb")
        self.key = key_file.read()
        key_file.close()

    def key_exists(self):
        key_file = Path(self.key_file_name)
        if key_file.is_file():
            return True
