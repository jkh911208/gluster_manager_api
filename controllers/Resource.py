import logging
import config
from db.Database import Database
import paramiko
from controllers.Credential import Credential

class Resource(object):
    def __init__(self):
        self.db = Database(config.mongodb_uri, config.database_name)
        self.db.set_collection("resource")

    def __del__(self):
        try:
            self.db.client.close()
        except Exception:
            pass

    def discover_new_node(self, node: dict) -> bool:
        # check if i have all the data i need
        # 5f1e4a06c9439c6a5b53649d -> correct
        # 5f1dfd04e83f7bbc21ea416a -> wrong
        print(node)
        required_key = ["address", "cred_id"]
        for key in required_key:
            if key not in node:
                raise ValueError("discover new node require address and credential id")
        
        # get credential detail from DB
        cred_tool = Credential()
        cred = cred_tool.get_one_credential_with_password(node["cred_id"])
        print(cred)

        # check if credential is correct
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node["address"], 22, cred["username"], cred["password"])

        # check if i have the sudo 

        # check Linux distro

        # check if address exist in db

        # write node infomation to DB
