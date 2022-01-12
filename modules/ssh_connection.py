from time import sleep
from paramiko import SSHClient,AutoAddPolicy
from scp import SCPClient


class ssh_connection:
    
   
    __shell=None
    __client_pre=None
    __Outstring=""

    def __del__(self):
        self.ssh_disconnect()

    #ssh connection
    
    def ssh_connect(self,args):
        try:
            
            self.__client_pre = SSHClient()
            self.__client_pre.set_missing_host_key_policy(AutoAddPolicy())
            self.__client_pre.connect(args.a,args.sshp,args.u,args.p,look_for_keys=False, allow_agent=False, auth_timeout=3)
            self.__shell=self.__client_pre.invoke_shell()    

            return self.__shell


        except:
            print("Failed to connect to SSH client")
            exit()

    #Upload file

    def scp_upload(self, filePath, remotePath):

        with SCPClient(self.__client_pre.get_transport())as scp:
            scp.put(filePath,remotePath,True)
            scp.close()
    
    #Send command to router

    def send_command(self,command):
        try:

            self.__shell.send(command+"\n")
            sleep(0.5)
            self.read_output()

            return self.__Outstring

        except Exception as e:
            print(e)
            exit()

    #Read output of router

    def read_output(self):
        try:

            while not self.__shell.recv_ready():
                sleep(1)
            self.__Outstring = self.__shell.recv(9999).decode("ascii").splitlines()

            return self.__Outstring
            
        except Exception as e:
            print(e)
            exit()

    #Close ssh connection

    def ssh_disconnect(self):

        if self.__shell:
            self.__shell.close()

        if self.__client_pre:
            self.__client_pre.close()