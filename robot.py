import os
import paramiko
from scp import SCPClient


import sys
import time


class Robot:
    def __init__(
        self,
        ip: str,
        port: int = 22,
        user: str = "root",
        password: str = "root",
        fileName: str = "log.json",
    ):
        self.ip: str = ip
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.fileName: str = fileName

    def checkIfAvailable(self, verbose: bool = True, counter=None):
        # print("Checking if", self.ip, "is available")
        response = os.system("ping -c 1 " + self.ip + " > /dev/null 2>&1")

        if response == 0:
            if verbose:
                print(f"{self.ip} is up!")
            return True
        else:
            if verbose:
                sys.stdout.write(f"\r{self.ip} is down!: " + f"\r{str(counter)}")
                sys.stdout.flush()
            # print(f"")
            return False

    def waitUntilAvailable(self):
        print("Connecting to", self.ip)
        counter: int = 0
        while not self.checkIfAvailable(verbose=True, counter=counter):
            counter += 1
        print("Connected to", self.ip)

    def createSSHConnection(self):
        print("Creating SSH connection to", self.ip)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip, self.port, self.user, self.password)
        return client

    def downloadLogs(self):
        print("Downloading logs from", self.ip)
        client = self.createSSHConnection()
        scp = SCPClient(client.get_transport())
        scp.get(self.fileName)
