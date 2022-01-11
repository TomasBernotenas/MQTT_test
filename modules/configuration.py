
class configuration:

    __shell=None
    __args=None
    back = "\033[F"

    def __init__(self,shell,args):
        self.__shell=shell
        self.__args=args

    def mqtt_package_install(self):

            print("Getting MQTT ready...                   "+self.back)

            self.__shell.send_command("opkg install http://opkg.teltonika-networks.com/523f276a5c096acb45908d716cf48116cdd7ab9e203c360868cc3acdcd5134e7/mosquitto-ssl_2.0.11-1_mips_24kc.ipk \n")
            self.__shell.send_command("opkg install http://opkg.teltonika-networks.com/523f276a5c096acb45908d716cf48116cdd7ab9e203c360868cc3acdcd5134e7/cJSON_1.7.14-3_mips_24kc.ipk \n")
            self.__shell.send_command("opkg install http://opkg.teltonika-networks.com/523f276a5c096acb45908d716cf48116cdd7ab9e203c360868cc3acdcd5134e7/vuci-app-mqtt_1_mips_24kc.ipk \n")
            self.__shell.send_command("opkg install http://opkg.teltonika-networks.com/523f276a5c096acb45908d716cf48116cdd7ab9e203c360868cc3acdcd5134e7/mqtt_pub_2021-11-12-1_mips_24kc.ipk \n")
            self.__shell.send_command("/etc/init.d/mosquitto restart\n") 
            self.__shell.send_command("/etc/init.d/mqtt_pub restart\n") 
            self.__shell.send_command("/etc/init.d/vuci restart\n") 
        

    def mqtt_broker_configuration(self):

       
        try:

            print("Configuring MQTT publisher...                   "+self.back)

            self.__shell.send_command("uci set mosquitto.mqtt.enabled=1")
            self.__shell.send_command("uci set mosquitto.mqtt.anonymous_access=1")
            self.__shell.send_command("uci set mosquitto.mqtt.local_port={0}".format(str(self.__args.cp)))
            self.__shell.send_command("uci set mosquitto.mqtt.use_tls_ssl=0")

            if self.__args.tls=="cert":

                self.__shell.send_command("uci set mosquitto.mqtt.use_tls_ssl=1")

            if self.__args.tls=="cert":     

                self.__shell.send_command("uci set mosquitto.mqtt.tls_type=cert")
                self.__shell.send_command("uci set mosquitto.mqtt.ca_file=/etc/certificates/ca.cert") 
                self.__shell.send_command("uci set mosquitto.mqtt.cert_file=/etc/certificates/{0}.cert".format(str(self.__args.a))) 
                self.__shell.send_command("uci set mosquitto.mqtt.key_file=/etc/certificates/{0}.key".format(str(self.__args.a)))
                self.__shell.send_command("uci set mosquitto.mqtt.tls_version=all")

            if self.__args.mqttauth.lower()=="true":

                self.__shell.send_command("uci set mosquitto.mqtt.password_file=/etc/certificates/mqtt_passwd")
                self.__shell.send_command("uci set mosquitto.mqtt.anonymous_access=0")

            else:

                self.__shell.send_command("uci delete mosquitto.mqtt.password_file")
                self.__shell.send_command("uci set mosquitto.mqtt.anonymous_access=1")

            self.__shell.send_command("uci commit mosquitto")
            self.__shell.send_command("/etc/init.d/mosquitto restart")

        except Exception as e:
            print(e)
            exit()

    def mqtt_publisher_configuration(self):

        try:

            print("Configuring MQTT broker...                            "+self.back)

            self.__shell.send_command("uci set mqtt_pub.mqtt_pub.enabled=1")
            self.__shell.send_command("uci set mqtt_pub.mqtt_pub.remote_addr={0}".format(self.__args.a))
            self.__shell.send_command("uci set mqtt_pub.mqtt_pub.remote_port={0}".format(str(self.__args.cp)))
            self.__shell.send_command("uci set mqtt_pub.mqtt_pub.tls=0")

            if self.__args.tls=="cert":

                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.tls=1")

            if self.__args.tls=="cert": 

                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.tls_type=cert")
                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.cafile=/etc/certificates/ca.cert") 
                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.certfile=/etc/certificates/{0}.cert".format(str(self.__args.a))) 
                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.keyfile=/etc/certificates/{0}.key".format(str(self.__args.a)))

            if self.__args.mqttauth.lower()=="true":

                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.username=admin") 
                self.__shell.send_command("uci set mqtt_pub.mqtt_pub.password=admin")

            else:

                self.__shell.send_command("uci delete mqtt_pub.mqtt_pub.username") 
                self.__shell.send_command("uci delete mqtt_pub.mqtt_pub.password")

            self.__shell.send_command("uci commit mqtt_pub")
            self.__shell.send_command("/etc/init.d/mqtt_pub  restart")

        except Exception as e:
            print(e)
            exit()
        

