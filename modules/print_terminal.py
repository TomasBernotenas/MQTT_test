

class print_terminal:

    def __init__(self):

        self.Passed=0
        self.Failed=0
        self.Total=0
    
    def term_print(self,ssh_client):

        CRED = '\033[91m'
        CGREEN  = '\33[32m'
        CEND = '\033[0m'
        back = '\033[F'
        
        try:

            Outsrting=ssh_client.shell.send_command("top -b -n1")[:3]
            
            print("                                                        \n")
            for line in Outsrting:
                print(line)

            print(CGREEN+"Passed: "+CEND + str(self.Passed) + CRED +"  Failed: " + CEND + str(self.Failed)+"  Total: " +str(self.Passed+self.Failed)+"\r")
            print(back*(len(Outsrting)+4))

        except Exception as e:
            print(e)
            print("Failed to print output to terminal")
            exit()

