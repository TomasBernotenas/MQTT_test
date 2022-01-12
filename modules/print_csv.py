from csv import writer

class print_csv:

    def __init__(self):

        self.counter=1
        self.result=None

    #Prints results to csv
   
    def print_to_csv(self,topics,deviceName,dateTime):
        try:    

            list=[]
            
            with open("results/" + str(deviceName) + "_" + dateTime + '.csv', 'a') as file:
                write = writer(file)

                for line in topics:
                    if line["Result"]=="Failed":
                        self.result=line["Result"]
                    list.append([line["topic"].upper(),line["MQTT info"],line["Router info"]])

                
                write.writerow(["Report Number: "+str(self.counter),])
                write.writerow(["TOPIC","MQTT INFO","ROUTER INFO"])    
                write.writerows(list)
                write.writerow([" "])
                write.writerow([" "])
                self.counter+=1

        except:
            exit()