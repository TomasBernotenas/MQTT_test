from time import sleep
import paho.mqtt.client as mqtt


class mqtt_connection:

    __client=None
    __client2=None
    __args=None
    __Outstring=[]
    __id=None

    
    def __init__(self,args):

        self.__client=mqtt.Client("")
        self.__client2=mqtt.Client("")
        self.__args=args

        if self.__args.mqttauth.lower()=="true":

            self.__client.username_pw_set("admin","admin")
            self.__client2.username_pw_set("admin","admin")

        if self.__args.tls=="cert": 

                self.__client.tls_set("./certificates/ca.cert")
                self.__client2.tls_set("./certificates/ca.cert")


        self.__id=self.mqtt_command(["id"])[0]

    def __del__(self):
        self.mqtt_disconnect()
        

    def on_message(self ,client, userdata, message):
        try:
            if str(message.payload.decode("utf-8")) != '':
                self.__Outstring.append(str(message.payload.decode("utf-8"))) 
            else:
                raise Exception("Returned MQTT value is empty in topic: {0}".format(message.topic))
        except Exception as e:
            print(e)
            exit()

        
    def mqtt_connect(self,client):
        try:
            client.connect(self.__args.a,int(self.__args.cp),15)
            
        except Exception as e:
            print(e)
            print("Failed to connect to MQTT")
            exit()


    def mqtt_disconnect(self):
        try:

            if self.__client:
                self.__client.disconnect()
            if self.__client2:
                self.__client2.disconnect()

        except Exception as e:
            print(e)

    def mqtt_command(self,topics):

        try:

            self.__Outstring=[]  
            self.__client.on_message=self.on_message

            self.mqtt_connect(self.__client)  
            sleep(0.5)

            self.__client.loop_start() 

            self.subscribe(topics)

            self.publish(topics)

            sleep(4) 

            self.__client.loop_stop()
            

            if self.__Outstring== '':
                self.mqtt_command(topics)
            
            print(self.__Outstring)
            return self.__Outstring
        except Exception as e:
            print(e)
            exit()


    def subscribe(self,topics):

        try:

            for line in topics:

                    if line=="id":
                        self.__client.subscribe("router/{0}".format(line))
                    else:
                        self.__client.subscribe("router/{0}/{1}".format(self.__id, line["topic"]))
        except:
            print("Failed to subscribe to topic")
            exit()

    def publish(self,topics):

        try:
            self.mqtt_connect(self.__client2)
            sleep(0.5)

            for line in topics:
                
                if line=="id":
                    self.__client2.publish("router/get",line)
                else:
                    self.__client2.publish("router/get",line["topic"])
        except:
            print("Failed to publish to MQTT")
            exit()
      
        
        
        