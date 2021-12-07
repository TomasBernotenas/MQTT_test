import os
from random import getrandbits
from modules.configuration import configuration
from modules.ssh_connection import ssh_connection
from modules.certificate_gen import certificate_gen
from modules.read_json import read_json



class router_acions:

    shell=None
    __args=None
    __topics=None
    __list=[]


    def  __init__(self,args,topics):

        self.shell=ssh_connection()
        self.__args=args
        self.shell.ssh_connect(self.__args)
        self.mqtt_conf()
        self.__topics=topics

    def __del__(self):
        del self.shell
        

    def mqtt_conf(self):
        
        try:

            conf = configuration(self.shell,self.__args)

            self.shell.send_command("stty -echo\n")

            if self.__args.d[:4].lower()=="rut9":
                conf.mqtt_package_install()

            if self.__args.tls=="cert":

                self.certificate_generation()

            if self.__args.mqttauth.lower()=="true":
                
                self.shell.scp_upload("./certificates","/etc")
                
            conf.mqtt_configuration()
            conf.mqtt_broker_configuration()

            del conf

        except Exception as e:
            print(e)
            exit()

    def certificate_generation(self):

        keyFile="certificates/"+str(self.__args.a)+".key"
        certFile="certificates/"+str(self.__args.a)+".cert"

        if not os.path.isfile('$(pwd)/'+keyFile) and not os.path.isfile('$(pwd)/'+certFile):

            certificates=certificate_gen(self.__args)
            certificates.issuerkey=certificates.createKeyPair()
            certificates.key=certificates.issuerkey
            certificates.issuer=certificates.request()
            certificates.issuer=certificates.cert_gen(serialNumber=getrandbits(64))
            certificates.key=certificates.createKeyPair()
            certificates.request(commonName=str(self.__args.a))
            certificates.cert_gen(serialNumber=getrandbits(64),KEY_FILE=keyFile,CERT_FILE=certFile)
            self.shell.scp_upload("./certificates","/etc")
            del certificates
            
    
    def router_info(self):
        
        self.__list=[]

        for line in self.__topics:

            temp = self.shell.send_command(line["config_command"])[0]
            temp = self.check_if_ubus(temp)
            self.__list.append(temp)

        return self.__list

    def check_if_ubus(self,Outsring):

        read=read_json()

        if "{" in Outsring:

            Outsring=read.ubus_load(Outsring)

        del read

        return Outsring
