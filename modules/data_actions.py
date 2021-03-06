from datetime import datetime
from modules.mqtt_connection import mqtt_connection
from modules.router_actions import router_acions
from modules.print_csv import print_csv
from modules.print_terminal import print_terminal
from modules.read_json import read_json

class data_actions:

    __mqtt_client=None
    __ssh_client=None
    __mqtt_Outstring=None
    __ssh_Outstring=None
    __args=None
    __topics=None
    __failed=0

    def __init__(self,args):

        topics=read_json.read_config(args.d)
        self.__ssh_client=router_acions(args,topics)
        self.__mqtt_client=mqtt_connection(args)
            
        self.__topics=topics
        self.__args=args

    #Gathers data from other modules
        
    def gather_data(self):
        try:

            dateTime= str(datetime.now())
            Terminal=print_terminal()
            csvPrinter= print_csv()

            while True:
            
                Terminal.term_print(self.__ssh_client)
                self.__mqtt_Outstring=self.__mqtt_client.mqtt_command(self.__topics)
                self.__ssh_Outstring=self.__ssh_client.router_info()
                sk=0

                for line in self.__topics:

                    line["MQTT info"]=self.__mqtt_Outstring[sk]
                    line["Router info"]=self.__ssh_Outstring[sk]
                    line["Result"]="Passed"
                    
                    if sk<=len(self.__mqtt_Outstring) and sk<=len(self.__ssh_Outstring):
                        sk+=1

                self.compare_data(Terminal,csvPrinter.counter)
                csvPrinter.print_to_csv(self.__topics,self.__args.d.upper(),dateTime)

        except Exception as e:
            print(e)
            exit()

    #compares mqtt and router info

    def compare_data(self,Terminal,repNumber):
        try:

            for line in self.__topics:
                
                if line["MQTT info"] != line["Router info"]:
                    if line["Router info"]!=" " and line["MQTT info"]!=" ":
                        try:
                            s=float(line["Router info"])-float(line["MQTT info"])
                        except:
                            s=10

                    else:
                        self.send_message(self.__args.tel,(" Device: {0} Empty result in report: {1}".format(self.__args.d.upper(), str(repNumber))))
                        self.set_result(line)
                        break

                    if line["topic"]=="uptime":

                        if s>8:

                            self.compare_data_result_action(line,repNumber)
                        break

                    if line["topic"]=="wan":
                        
                        self.compare_data_result_action(line,repNumber)
                        break
                      
                    elif -10>s>10:

                        self.compare_data_result_action(line,repNumber)

            if self.__failed>0:
                Terminal.Failed+=1
            else:
                Terminal.Passed+=1

                    
        except Exception as e:
            print(e)
            exit()

    #Actions after info dosent match

    def compare_data_result_action(self,line,repNumber):
        self.send_message(self.__args.tel,(" Device: {0} Topic: {1} dosent match report number: {2}".format(self.__args.d.upper(), line["topic"], str(repNumber))))
        self.set_result(line)

    #Sends message

    def send_message(self,phone,message):
        self.__ssh_client.shell.send_command("gsmctl -S -s "+"\"{0} {1}\"".format(phone, message))

    #Sets result in the info array

    def set_result(self,line):

        self.__failed+=1
        line["Result"]="Failed"

