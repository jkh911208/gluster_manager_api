import config
from db.Database import Database
from controllers.Cryptography import Crypto

class Credential(object):
    def __init__(self):
        self.db = Database(config.mongodb_uri, config.database_name)
        self.db.set_collection("credential")

    def __del__(self):
        try:
            self.db.client.close()
        except Exception:
            pass

    def get_all_credentials(self) -> dict:
        credentials = self.db.find_all({ "_id": 1, "name": 1, "username": 1 })
        for cred in credentials:
            # convert ObjectId to string
            cred["_id"] = str(cred["_id"])
        credentials = {"credentials" : credentials}
        return credentials

    def create_credential(self, data: dict) -> bool:
        # check if i have all the data i need
        required_key = ["name", "username", "password"]
        for key in required_key:
            if key not in data:
                raise ValueError("credential need name, username and password")

        # check if name exist in db
        exist_data = self.db.find({"name": data["name"]})
        if len(exist_data) > 0:
            raise ValueError("Same name for credential already exist in DB")

        # encrypt the password
        crypto_tool = Crypto()
        data["password"] = crypto_tool.encrypt(data["password"])
        return self.db.insert(data)

    def get_one_credential_with_password(self, id) -> dict:
        crypto_tool = Crypto()
        credential = self.db.find_by_id(id)
        credential["password"] = crypto_tool.decrypt(credential["password"])
        return credential
