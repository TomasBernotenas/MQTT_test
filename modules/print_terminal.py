

class print_terminal:

    def __init__(self):

        self.Passed=0
        self.Failed=0
        self.Total=0

    # prints information to the terminal
    
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
            print("{0}Passed: {1} {2} {3} Failed: {4} {5} Total: {6} \r".format(CGREEN,CEND,str(self.Passed),CRED,CEND,str(self.Failed),str(self.Passed+self.Failed)))
            print(back*(len(Outsrting)+4))

        except Exception as e:
            print(e)
            print("Failed to print output to terminal")
            exit()

