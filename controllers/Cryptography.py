import config
from cryptography.fernet import Fernet
from db.Database import Database

class Crypto(object):
    def __init__(self):
        self.db = Database(config.mongodb_uri, config.database_name)
        self.db.set_collection("Cryptography")
        self.secret = self.__get_secret()

    def __del__(self):
        try:
            self.db.client.close()
        except Exception:
            pass

    def __find_secret_from_db(self):
        query = { "secret_key": {"$exists": 1}}
        secrets = self.db.find(query)
        temp = []
        for secret in secrets:
            if len(secret) == 2:
                temp.append(secret)

        if len(temp) > 1:
            raise RuntimeError("There is more than one secret in the DB")
        elif len(temp) == 1:
            return temp[0]["secret_key"]
        else:
            return None

    def __gen_secret(self):
        existing_secret = self.__find_secret_from_db()
        if existing_secret is not None:
            return existing_secret

        secret = Fernet.generate_key()
        self.db.insert({"secret_key": secret})
        return secret

    def __get_secret(self):
        existing_secret = self.__find_secret_from_db()
        if existing_secret is not None:
            return existing_secret

        return self.__gen_secret()

    def encrypt(self, data: str):
        fernet = Fernet(self.secret)
        return fernet.encrypt(data.encode())

    def decrypt(self, data: str):
        fernet = Fernet(self.secret)
        return fernet.decrypt(data).decode()