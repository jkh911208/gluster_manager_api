from util.Encryption import Encryption

class Credential(object):
    def __init__(self, db):
        self.db = db
        self.collection = self.db.set_collection("credential")

    def create_credential(self, data: dict) -> bool:
        # check if i have all the data i need
        required_key = ["name", "username", "password"]
        for key in required_key:
            if key not in data:
                raise ValueError("credential need name, username and password")

        # check if name exist in db
        exist_data = self.db.find({"name": data["name"]})
        print(exist_data)
        if len(exist_data) > 0:
            raise ValueError("Same name for credential already exist in DB")

        # encrypt the password
        encrypt_tool = Encryption()
        data["password"] = encrypt_tool.encrypt(data["password"])
        return self.db.insert(data)

    def get_all_credentials(self) -> dict:
        credentials = self.db.find_all({ "_id": 1, "name": 1, "username": 1 })
        for cred in credentials:
            # convert ObjectId to string
            cred["_id"] = str(cred["_id"])
        credentials = {"credentials" : credentials}
        return credentials