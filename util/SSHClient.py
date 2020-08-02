import paramiko
import time

class SSHClient(object):
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.address, 22, self.username, self.password)
        self.shell = self.ssh.invoke_shell()

    def __del__(self):
        self.ssh.close()

    def check_sudo_privilege(self):
        result = self.command("sudo -v")
        if "Sorry" in result:
            return False
        return True

    def change_to_su(self):
        if not self.am_i_su():
            self.command_with_shell("sudo su")
            self.command_with_shell(self.password)

    def am_i_su(self) -> bool:
        result = self.command_with_shell("\x03")
        if result[-1].endswith("# "):
            return True
        return False

    def command_with_shell(self, command: str, shell=None, byte=False) -> list:
        if shell is None:
            shell = self.shell
        shell.sendall(command + "\n")
        while not shell.recv_ready():
            time.sleep(0.1)
        time.sleep(1)
        output = shell.recv(99999)
        if not byte:
            output = output.decode("utf-8")
            output = output.replace("\r", "")
            output = output.split("\n")
        return output

    def command(self, command: str) -> list:
        shell = self.ssh.invoke_shell()
        output = self.command_with_shell(command, shell)
        shell.close()
        return output
