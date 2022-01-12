from json import load,loads

class read_json:

    #Reads .json file

    def read_config(deviceName):
        try:

            topics = None

            with open("config.json","r") as file:

                devices = load(file)

                for dev in devices["devices"]:
                    if deviceName.lower() in dev["device"].lower():

                        topics = dev["topics"] 
                        break
                    
            if topics==None:    
                raise TypeError

            return topics  
              
        except TypeError:
            print("There is no such device in configuration file")
            exit()

    #Proccess ubus info

    def ubus_load(self,Outsring):

        temp = loads(Outsring)

        try:

            Outsring=temp["value"]

            return Outsring

        except:

            try:

                Outsring=temp["uptime"]

                return Outsring

            except:
                pass
        