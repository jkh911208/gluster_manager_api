from cryptography.fernet import Fernet
import config

class Encryption(object):
    def __init__(self):
        self.secret = config.secret

    def encrypt(self, data: str):
        encoded_message = data.encode()
        fernet = Fernet(self.secret)
        encrypted_message = fernet.encrypt(encoded_message)
        return encrypted_message

    def decrypt(self, data: str):
        fernet = Fernet(self.secret)
        decrypted_message = fernet.decrypt(data)
        return decrypted_message.decode()
