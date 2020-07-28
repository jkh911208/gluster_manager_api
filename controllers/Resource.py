import logging
import config
from db.Database import Database
import paramiko
from controllers.Credential import Credential
from util.SSHClient import SSHClient

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
        required_key = ["address", "cred_id"]
        for key in required_key:
            if key not in node:
                raise ValueError("discover new node require address and credential id")
        
        # get credential detail from DB
        cred_tool = Credential()
        cred = cred_tool.get_one_credential_with_password(node["cred_id"])

        # initiate ssh connection
        ssh = SSHClient(node["address"], cred["username"], cred["password"])

        # check if user have sudo privilege

        # check Linux distro

        # check if address exist in db

        # write node infomation to DB