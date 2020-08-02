from controllers.Credential import Credential
from util.SSHClient import SSHClient

def get_disk_list(address: str, cred_id: str) -> list:
    cred_controller = Credential()
    cred = cred_controller.get_one_credential_with_password(cred_id)

    ssh = SSHClient(address, cred["username"], cred["password"])

    ssh.change_to_su()
    ssh.command_with_shell("sudo lshw -class disk")

    