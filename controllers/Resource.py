import logging
import config
from db.Database import Database
from controllers.Credential import Credential
from util.SSHClient import SSHClient
import util.convert_to_dict
import util.inventory

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
        if not ssh.check_sudo_privilege():
            raise RuntimeError("User don't have sudo previlege")

        # check Linux distro
        distro = ssh.command("cat /etc/os-release")
        distro = util.convert_to_dict.config_to_dict(distro)
        try:
            if distro["ID"] != "centos":
                raise RuntimeError("Only support CentOS 7")
            if int(distro["VERSION_ID"]) != 7:
                raise RuntimeError("Only support CentOS 7")
        except KeyError as err:
            logging.exception("cannot verify the linux distro : {}".format(distro))
            raise RuntimeError("Only support CentOS 7")

        # get disk list in dict
        disk_list = util.inventory.get_disk_list(ssh)

        # check if address exist in db
        exist_data = self.db.find({"address": node["address"]})
        if len(exist_data) > 0:
            raise ValueError("node is already discovered")

        # write node infomation to DB
        return self.db.insert({
            "address" : node["address"],
            "cred_id" : node["cred_id"],
            "distro" : distro["ID"],
            "version" : int(distro["VERSION_ID"]),
            "name" : distro["PRETTY_NAME"] if "PRETTY_NAME" in distro else distro["ID"] + " " + distro["VERSION_ID"],
            "disks": disk_list
        })
    
    def get_all_nodes(self):
        nodes = self.db.find_all()
        for node in nodes:
            # convert ObjectId to string
            node["_id"] = str(node["_id"])
        nodes = {"nodes" : nodes}
        return nodes

    def delete_one_node(self, node_id):
        # check if i have all the data i need
        required_key = ["id"]
        for key in required_key:
            if key not in node_id:
                raise ValueError("delete node requires id")

        #TODO
        # Need to add check if node is in use for cluster. if yes do not delete
        
        self.db.delete(node_id["id"])