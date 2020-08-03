import logging
import json

def get_disk_list(ssh) -> list:
    # ssh = SSHClient(address, username, password)

    ssh.change_to_su()
    which_lshw = ssh.command_with_shell("which lshw")
    if not which_lshw[1].endswith("/lshw"):
        logging.warning("installing lshw in node : {}".format(address))
        ssh.command_with_shell("sudo install lshw -y")

    # get all disk in the disk in the node
    disks = ssh.command_with_shell("lshw -json -class disk", byte=True)
    disks = disks.decode("utf-8")
    disks = disks[disks.find("{"):disks.rfind("}")+1].replace("\r", "").replace("\n", "").replace(" ", "")
    disk_list = []
    while True:
        location = disks.find("},{")
        if location == -1:
            disk_list.append(json.loads(disks))
            break
        disk_list.append(json.loads(disks[:location + 1]))
        disks = disks[location + 2:]

    return disk_list