# src/informatica_cli/config.py
import json
from pathlib import Path
from cryptography.fernet import Fernet

CONFIG_DIR = Path('./config')
CONFIG_FILE = CONFIG_DIR / 'config.json'

DEFAULT_CONFIG = {
    "pod": None,
    "region": None,
    "username": None,
    "password": None,
    "key": None,
    "sessionId": None,
    "maxAttempts": 5,
    "pageSize": 100
}

class Config:
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.data = {}
        self.load()

    def load(self):
        if not self.config_path.exists():
            self.data = DEFAULT_CONFIG.copy()
            
            # Generate the once off key for encryption and decryption
            self.data['key'] = Fernet.generate_key().decode('utf-8')
            
            self.save()
        else:
            with open(self.config_path, 'r') as f:
                self.data = json.load(f)

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        
        # If returning the password, first decrypt it using the key
        if key == 'password':
            cipher_key = self.data.get('key').encode('utf-8')
            cipher_suite = Fernet(cipher_key)
            encrypted = self.data.get(key, '')
            if encrypted:
                return cipher_suite.decrypt(self.data.get(key, '')).decode('utf-8')
            else:
                return encrypted
        else:
            return self.data.get(key, default)

    def set(self, key, value):
        
        # If setting the password, encrypt it using the key
        if key == 'password':
            if value:
                cipher_key = self.data.get('key', '')
                cipher_suite = Fernet(cipher_key)
                self.data[key] = cipher_suite.encrypt(value.encode('utf-8')).decode('utf-8')
            else:
                self.data[key] = None
        else:
            self.data[key] = value
        
        self.save()

# Expose the class as a variable
config = Config()